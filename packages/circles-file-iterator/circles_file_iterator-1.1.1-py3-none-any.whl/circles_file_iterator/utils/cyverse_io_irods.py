import subprocess
import os
import ssl
from irods.session import iRODSSession
from .cache import remove_file_from_cache
import json


# implementation of the python client found here:
# https://github.com/irods/python-irodsclient


def create_irods_env(username: str, local_user_folder: str) -> str:
    env_path = os.path.join(local_user_folder, '.irods', 'irods_environment.json')
    folder_path = os.path.join(local_user_folder, '.irods')

    folder_exists = os.path.exists(folder_path)

    if not folder_exists:
        # if the config file doesn't exist, we create the folder and environment file
        os.mkdir(folder_path)

    env_data = {
        "irods_zone_name": "iplant",
        "irods_host": "data.cyverse.org",
        "irods_port": 1247,
        "irods_user_name": username
    }

    with open(env_path, 'w', encoding='utf-8') as f:
        json.dump(env_data, f, ensure_ascii=False, indent=4)

    return env_path


def getIRODSSession(timeout = 300):
    '''
    Returns an IRODS logged in session.
    The session parameters can either be loaded from '~/.irods/irods_environment.json' (default)
    Or from the file given by the environment variable: 'IRODS_ENVIRONMENT_FILE'

    :parameter timeout: number of seconds where the connexion will be active.
    defaults to 300, turn up if you need to handle larger files download/uploads
    :return: irodsclient session object

    TODO: handle new way of getting the connexion in Docker container!
    '''
    try:
        try:
            env_file = os.environ['IRODS_ENVIRONMENT_FILE']
            # Nope doesn't exist locally. Could be useful for indicating that to Docker container environment
            # for docker, use a create_environment file method!?
            # TODO: question for Jonathan over which account to keep!
        except KeyError:
            env_file = os.path.expanduser('~/.irods/irods_environment.json') # OK this file exists
        ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
        ssl_settings = {'ssl_context': ssl_context}
        with iRODSSession(irods_env_file=env_file, **ssl_settings) as session:
            # make the connexion longer
            session.connection_timeout = timeout
            # returns the session object
            return session
    
    except Exception as e:
        raise Exception(f'Creation of the IRODS Session object failed on: {e}')


async def IRODSGet(remote_address: str, cache_address: str, session = None):
    '''
    Wrapper for getting files through IRODS
    :param remote_address: address on CyVerse to pull the file from
    :param cache_address: local address to download the file into
    :param session: python-irodsclient session object. If not provided, creates it automatically.
    :return: downloads the file locally to cache_address, and retrieve its address
    '''
    # address formatting -> no need
    # example: >>> logical_path = "/{0.zone}/home/{0.username}/{1}".format(session,"myfile.dat")
    # here we can just check if the session has the right zone and username
    try:
        if not session:
            session = getIRODSSession()
        assert session.zone == 'iplant'

        session.data_objects.get(remote_address, cache_address)

        filename = remote_address.split('/')[-1]

        return f'{cache_address}/{filename}'
    
    except Exception as e:
        raise Exception(f'Error trying to download file from CyVerse through IRODS. Failed on: {e}')


async def IRODSPut(remote_address: str, local_address: str, session = None, clean_file_from_cache = False, new_object: bool = True, verbose: bool = False):
    '''
    Wrapper for uploading files through IRODS
    :param remote_address: address on CyVerse to push the file to
    :param local_address: local address of the file to upload.
        (WARNING: DO NOT PUT A RELATIVE PATH, USE ABSOLUTE PATH!)
    :param session: python-irodsclient session object.  If not provided, creates it automatically.
    :param clean_file_from_cache: Defaults to False. If True, remove the file from cache after successful upload.
    :param new_object: Defaults to True. Set to false if you only want to modify an existing data object in CyVerse
    :return: uploads the file to remote_address, and retrieve its remote address
    '''
    try:
        if not session:
            session = getIRODSSession()
        assert session.zone == 'iplant'

        if verbose:
            print(f'iput args are: \nlocal: {local_address}\nremote: {remote_address}')

        session.data_objects.put(local_address, remote_address)

        if clean_file_from_cache:
            if ('/temp_cache/' in local_address) or ('/long_cache/' in local_address):
                remove_file_from_cache(local_address)
            else:
                raise Exception(f'Cannot remove a file not located inside of the temporary cache.\nThe desired file to remove is located at: {local_address}')

        return remote_address
    
    except Exception as e:
        raise Exception(f'Error trying to upload file to CyVerse through IRODS. Failed on: {e}')


