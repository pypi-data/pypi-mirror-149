from ast import literal_eval
from typing import List
import pandas as pd
from .cache import get_all_files_from_cache_dir
from .cyverse_io_irods import IRODSGet
from .cache import init_cache
from .cyverse_files import findall_files
from ..global_variables.global_variables import cyverse_path_server_resources_default, local_long_folder, local_temp_folder, cyverse_path_server_resources_user


class FileIteratorCanGps:
    """
    Class handling file download and caching, csv filtering and time cuts
    Works for retrieving files using CAN+GPS CSV data (from CyVerse runs)
    """
    # ============================== ATTRIBUTES ==============================

    data = None
    current_remote_adresses = None
    current_file = None
    can_local_address = None
    gps_local_address = None
    index = None
    max_index = None
    previous_cut_time = None
    next_cut_time = None
    exploration_used = None
    before_next = None
    after_next = None


    # ============================== METHODS ==============================

    def __init__(self):
        self.index = 0


    def __str__(self):
        if self.max_index is None:
            return f'File Iterator configuration is not finished. Please select an exploration to use.'
        else:
            return f'File Iterator is set with {self.max_index} files ready to be served.\
                    \nThe file exploration used is: {self.exploration_used}\
                    \nCurrent index is: {self.index}\
                    \nCut times are: before: {self.previous_cut_time}, after: {self.next_cut_time}'


    # -------------- Getting and setting which exploration to use --------------

    def set_exploration_to_use(self, local_exploration_to_use: str) -> None:
        '''
        Sets which exploration (available locally) to use
        :param local_exploration_to_use: path to the exploration CSV to use
        '''
        self.exploration_used = local_exploration_to_use
        self.data = pd.read_csv(local_exploration_to_use)
        self.max_index = len(self.data)


    async def get_default_explorations(self, clear_long_cache: bool = False) -> None:
        '''
        Gets from CyVerse the default explorations of CSV CAN+GPS path couples

        :param clear_long_cache: Set to true to clear the cache before downloading those default explorations
        :return: void
        '''
        if clear_long_cache:
            init_cache(long=True)

        files = findall_files(root=cyverse_path_server_resources_default)

        for file in files:
            await IRODSGet(remote_address=file, cache_address=local_long_folder)


    def find_available_user_explorations(self) -> List[str]:
        '''
        Find the path to all the user explorations.
        Useful to call the method get_specific_user_exploration() and use a specific user defined exploration path.

        :return: List of remote path (on CyVerse) of the available user explorations
        '''
        files = findall_files(root=cyverse_path_server_resources_user)
        return files


    def find_locally_available_explorations(self) -> List[str]:
        '''
        Gives the path to all the local explorations, already downloaded locally.
        Use this to select the right exploration to use for your file-to-file analysis.

        '''
        files = get_all_files_from_cache_dir(long=True)
        return files


    async def get_specific_user_exploration(self, remote_path: str, clear_long_cache: bool = False) -> str:
        '''
        Gets from CyVerse the default explorations of CSV CAN+GPS path couples
        :param remote_path: path to CyVerse user exploration
        :param clear_long_cache: Set to true to clear the cache before downloading those default explorations
        :return: Local path where the exploration has been downloaded
        '''
        if clear_long_cache:
            init_cache(long=True)

        local_path_exploration = await IRODSGet(remote_address=remote_path, cache_address=local_long_folder)

        self.exploration_used = local_path_exploration
        self.data = pd.read_csv(local_path_exploration)
        self.max_index = len(self.data)

        return local_path_exploration


    # -------------- Filtering --------------

    def filter(self, date: str = None, vin: str = None, ):
        """
        filter the rows based on those criteria

        :param vin: list of acceptable vehicle identification numbers
        :param date: string formatted as YYYY-MM-DD. Keep only the runs from this day

        :return: None. Only updates self.data to only keep the desirable instances
        """

        if date is not None:
            filter_array_date = [(date in literal_eval(name)['can']) for name in self.data['Files']]
            self.data = self.data.loc[filter_array_date]
        if vin is not None:
            filter_array_vin = [(vin in literal_eval(name)['can']) for name in self.data['Files']]
            self.data = self.data.loc[filter_array_vin]

        self.max_index = len(self.data)


    # -------------- Next hook methods --------------

    def set_hook_before_next(self, before_next):
        self.before_next = before_next

    def set_hook_after_next(self, after_next):
        self.after_next = after_next


    # -------------- Retrieving file through next() method --------------

    async def next(self, ignore_gps_file: bool = True, verbose: bool = False):
        """
        clears cache & downloads the next couple of files
        :param: ignore_gps_file: set to True to avoid downloading the GPS file
        :return: - object with paths to the downloaded CAN and GPS file
                 - if the maximum index is reached, returns an exception as:
                    Exception('max_index')
        """
        try:
            if verbose:
                print(f'serving and preprocessing file, number {self.index} out of {self.max_index - 1}')
            if self.index < self.max_index:
                if self.before_next is not None:
                    self.before_next(self)

                init_cache()

                self.current_file = self.data.iloc[self.index]['Files']
                self.current_remote_adresses = literal_eval(self.current_file)['can']

                self.can_local_address = await IRODSGet(self.current_remote_adresses, local_temp_folder)

                if ignore_gps_file:
                    self.gps_local_address = None
                else:
                    self.gps_local_address = await IRODSGet(self.current_remote_adresses, local_temp_folder)

                self.index += 1

                if verbose:
                    print(f'Download and preprocessing of {self.can_local_address} was successful')

                if self.after_next is not None:
                    self.after_next(self)

                print('inside', self.can_local_address, self.current_remote_adresses)
                if ignore_gps_file:
                    return self.can_local_address, self.current_remote_adresses
                else:
                    return {"can": self.can_local_address, "gps": self.gps_local_address}
            else:
                raise Exception('max_index')

        except Exception as e:
            raise Exception(f'Downloading next file failed on {e}')

    def reset(self):
        '''
        Resets the index to 0.
        '''
        self.index = 0


    '''
    # ---------------------------------------------------------------------------------------------------------
    #
    # NOTE: This legacy code can be used to create file iterator over the events, I.E using an event analysis
    # instead of the file iterator to get the CAN files from cyverse corresponding to different events, and cut
    # them around the time of the different events.
    #
    # You also need to add this import at the top to have access to the functions performing CSV cutting
    #     from .csv_cutting import perform_cut, find_ts_time_close
    #
    # ---------------------------------------------------------------------------------------------------------

    def filter(self, cc_state: List[int] = None, speed: Dict[str, int] = None, vin: List[str] = None, date: Dict[str, str] = None, event_type: List[str] = None):
        """
        filter the rows based on those criteria
        :param cc_state: list of acceptable controller state values
        :param speed: {min: int min_speed in km/h, max: int max_speed in km/h}
        :param vin: list of acceptable vehicle identification numbers
        :param date: {beg: date, end: date}, with date as strings, formatted as YYYY-MM-DD-HH-MM-SS
        :param event_type: list of acceptable event types. possible event types are:
            - car_crossing
            - <more to come in the future>
        :return: updates self.data to only keep the desirable instances
        """
        if event_type is not None:
            self.data = self.data.loc[self.data['event_type'] in event_type]
        if vin is not None:
            self.data = self.data.loc[self.data['vin'] in vin]
        if cc_state is not None:
            self.data = self.data.loc[self.data['event_cc_state'] in cc_state]
        if speed is not None:
            self.data = self.data.loc[(self.data['event_speeds'] >= speed['min'])
                                  & (self.data['event_speeds'] >= speed['min'])]
        if date is not None:
            self.data = self.data.loc[(self.data['date'] >= date['min'])
                                  & (self.data['date'] >= date['min'])]
        self.max_index = len(self.data)


    # -------------- Cutting --------------

    def set_cut(self, previous, next):
        """
        sets the values of the parameters of the cut for the csv CAN/GPS files
        :param previous: number of seconds kept before the event
        :param next: number of seconds kept after the event
        :return: void. updates the attributes of the file server
        """
        self.previous_cut_time = previous
        self.next_cut_time = next

    def cut_can_file(self):
        """
        cut the current file according to the cutting parameters defined
        """
        event_time = self.current_event['event_time']
        can_new_path = perform_cut(self.can_local_address, self.previous_cut_time, self.next_cut_time, event_time)
        gps_new_path = None
        if self.gps_local_address is not None:
            gps_new_path = perform_cut(self.can_local_address, self.previous_cut_time, self.next_cut_time, event_time)
        return {
            'can': can_new_path,
            'gps': gps_new_path,
        }
    '''

