from datetime import datetime
import os
from typing import List
from .cyverse_files import findall_files
from .cyverse_io_irods import IRODSPut
import pandas as pd
from ..global_variables.global_variables import cyverse_path_server_resources_user, local_long_folder


def read_metadata_from_exploration_name(filename: str):
    '''
    :param filename: name of the file onto which extract metadata
    :return: Dict object with those fields:
    {
        filename: <>,
        name: <>,
        created_on: <>,
        root: <>, 
    }
    NOTE: the root file has _ instead of /
    '''
    splitted_filename = filename.split('&')
    return {'filename': filename, 'name': splitted_filename[1], 'created_on': splitted_filename[2].split('=')[1], 'root': splitted_filename[3].split('=')[1]}


def can_gps_coupling(files: List[any]):
    '''
    links the CAN and GPS from same acquisitions
    :param files: array of file adresses
    :return: List<{'can': str, 'gps': str || None}>
    '''
    file_list = []

    for file in files:
        if '_CAN_Messages.csv' in file:
            file_list.append({'can': file, 'gps': None})

    for i in range(len(file_list)):
        file_gps = file_list[i]['can'][0:-17] + '_GPS_Messages.csv'
        if file_gps in files:
            file_list[i]['gps'] = file_gps

    return file_list


def coupled_files_file_namer(name: str, root: str):
    root_mod = root.replace("/", "_").replace("'", "")
    if root_mod[-4:] == '.csv':
        root_mod = root_mod[:-4]
    name_mod = name.replace("'", "")

    return f'file_exploration&{name_mod}&created_on={str(datetime.now()).replace(" ", "_")}&root={root_mod}.csv'


async def create_fileshare_exploration_can_gps(root: str, exploration_name: str, verbose: bool = False):
    '''
    Creates a new fileshare exploration for CAN / GPS coulped files.
    The exploration locally stored in the folder given by the global variable local_long_folder.
    It is also uploaded to CyVerse in the user-created explorations folder, '/iplant/home/noecarras/resources_file_iterator/user/'.

    :param root: root of the exploration to consider (on CyVerse)
    :param exploration_name: name to give to the exploration
    :param verbose: set to True to have more extensive log
    :return: the address of the newly created file on CyVerse
    '''
    # explores the folders to find CSV pairs of CAN & GPS files
    all_files = findall_files(
        root,
        authorized_file_extensions=['csv'],
        unauthorized_folder_leaves=['bagfiles', 'dashcams'],
        verbose=verbose
    )

    coupled_files = can_gps_coupling(all_files)

    # save the csv file
    output_filename = coupled_files_file_namer(exploration_name, root)
    local_file_path = os.path.join(local_long_folder, output_filename)
    if verbose:
        print(local_file_path)

    df = pd.DataFrame(data={'Files': coupled_files})
    df.to_csv(path_or_buf=local_file_path)
    if verbose:
        print('exploration logged as: ', output_filename)
    
    # uploads to CyVerse, to remote_exploration_address
    # & init the local cache after upload
    remote_name = await IRODSPut(
        remote_address=os.path.join(cyverse_path_server_resources_user, output_filename),
        local_address=local_file_path,
        clean_file_from_cache=True,
        verbose=verbose
    )

    # returns the address on CyVerse, returns remote_exploration_address
    return remote_name
