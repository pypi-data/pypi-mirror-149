import os
import subprocess
from typing import List
from ..global_variables.global_variables import local_temp_folder, local_long_folder

def init_cache(long: bool = False) -> str:
    '''
    clears the temp cache if exists and initialises it
    :param long: set to true to initialize the long lasting cache folder.
    :return: cache address
    '''
    try:
        if long:
            cache = local_long_folder
        else:
            cache = local_temp_folder

        subprocess.run(['rm', '-r', cache],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)

        subprocess.run(['mkdir', cache],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True)

        return cache
    
    except Exception as e:
        raise Exception(f'Error while trying to init cache.\nFailed on: {e}')
    

def remove_file_from_cache(file_address: str) -> str:
    '''
    Removes one file locally from path
    :param file_address: Path to the file to delete. It needs to be located either in temp_cache or long_cache to be deleted.
    :return: file_address once the file has been deleted.
    '''
    try:
        if (file_address) and (('temp_cache' in file_address) or ('long_cache' in file_address)):
            subprocess.run(['rm', file_address],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)
            return file_address
        
        else:
            raise Exception(f'file not located in cache folders. File has not been deleted')
    
    except Exception as e:
        raise Exception(f'Error while trying to remove {file_address} from Cache.\nFailed on: {e}')


def get_all_files_from_cache_dir(long: bool = False) -> List[str]:
    '''
    :param long: set to true to target the long lasting cache folder.
    :return: List of path to the files within the root
    '''
    try:
        if long:
            cache = local_long_folder
        else:
            cache = local_temp_folder
    
        files = [os.path.join(cache, f) for f in os.listdir(cache) if os.path.isfile(os.path.join(cache, f))]
        return files

    except Exception as e:
        raise Exception(f'Finding files in {cache} failed on {e}')
