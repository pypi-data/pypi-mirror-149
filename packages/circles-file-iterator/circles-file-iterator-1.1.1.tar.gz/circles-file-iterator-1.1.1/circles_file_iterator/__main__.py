import sys
import os
from .utils.cyverse_io_irods import create_irods_env


def main():
    sys.stdout.write(f'Configuration of the File Iterator package.\n')
    #    Please Write down your CyVerse username: ')
    username = input('Please Write down your CyVerse username: ')
    #sys.stdout.write(f'Please write down the absolute path to the root folder of your project: ')
    in_local_folder_path = input('Please write down the absolute path to the root folder of your project: ')
    local_folder_path = os.path.abspath(in_local_folder_path.strip())
    #sys.stdout.write(f'Please write down the absolute path to your user folder root: ')
    in_user_folder_root = input(f'Please write down the absolute path to your user folder root: ')
    user_folder_root = os.path.abspath(in_user_folder_root.strip())
    
    try:
        global_vars = open(os.path.abspath('./venv/lib/python3.7/site-packages/circles_file_iterator/global_variables/global_variables.py'), 'r+').readlines()
        out_filename = open(os.path.abspath('./venv/lib/python3.7/site-packages/circles_file_iterator/global_variables/global_variables.py'), 'w')
        for l in global_vars:
            if l[:15] == 'local_folder = ':
                out_filename.write(l[:15] + "'" + local_folder_path + "'" + "\n")
            else:
                out_filename.write(l)
        
        os.mkdir(os.path.join(local_folder_path, 'temp_cache'))
        os.mkdir(os.path.join(local_folder_path, 'long_cache'))

        irods_file_env = create_irods_env(username=username, local_user_folder=user_folder_root)
    
    except Exception as e:
        raise Exception(f'Configuration failed on: {e}')

    sys.stdout.write(f'IRODS configuration has been written to {irods_file_env}.\n\
        Local cache file has been set to be in {local_folder_path}\n\
        Your CyVerse usename has been read with success.')


if __name__ == "__main__":
    main()