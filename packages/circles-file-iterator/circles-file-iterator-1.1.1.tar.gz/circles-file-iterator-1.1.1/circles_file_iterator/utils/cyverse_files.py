import subprocess
from typing import List


def ils():
    '''
    wrapper for iRODS ils command
    :return: list of files and folder in the current folder
    '''
    process_files = subprocess.run(['ils'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   universal_newlines=True)
    files = process_files.stdout.split(sep='\n')[1:-1]
    return [f.strip() for f in files]


def icd(destination):
    '''
    wrapper for iRODS icd command
    :param destination: destination to which go to
    :return: subprocess output
    '''
    return subprocess.run(['icd', destination],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True)


def ipwd(verbose=False):
    '''
    wrapper for iRODS ipwd command
    :param verbose: set to True for more logs
    :return: current directory on CyVerse
    '''
    pwd = subprocess.run(['ipwd'],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          universal_newlines=True)
    out = pwd.stdout.strip().strip('\n')
    if verbose:
        print('pwd output is:', out)
    return out


def findall_files(root, authorized_file_extensions: List[str] = ['csv'], unauthorized_folder_leaves: List[str] = ['bagfiles', 'dashcams'], verbose: bool = False):
    '''
    finds all files within the root directory and recursively below

    :param root: str, root file from which to begin the search
    :param authorized_file_extensions: Select the extensions you which to reference the files from.
        Give as a list of the authorized extensions
    :param unauthorized_folder_leaves: Select between bagfiles, dashcams, libpanda.
        Give a list of the folders you which to choose. Defaults to only take libpandas.
    :param verbose: bool, set to True to see fuller logs

    :return: List<str> of the file addresses found on CyVerse
    '''
    dir_queue = [root]
    files = []

    while len(dir_queue) != 0:

        current_dir = dir_queue.pop()
        icd(current_dir)
        queue = ils()

        if verbose:
            print('---------')
            print('current queue dir: ', dir_queue)
            print('current directory is: ', current_dir)
            print('current file queue is: ', queue)

        for f in queue:
            if verbose:
                print('current file tests on: ', f, ' \nIs folder? : ', f[0:2], ' \nand extension is: ', f.split('.')[-1])
            # avoid unauthorized folders
            isFolder = (f[0:2] == 'C-')
            isAuthorized = True
            for unauth_folder in unauthorized_folder_leaves:
                if unauth_folder in f:
                    isAuthorized = False            

            if isFolder and isAuthorized:
                dir_queue.append(f[3:])
                if verbose:
                    print('appending dir queue; ', f)
            
            elif f.split('.')[-1] in authorized_file_extensions:
                # We also conserve the current folder to get the entire path to the file
                current_folder = ipwd()
                files.append(f'{current_folder}/{f}')
                if verbose:
                    print('appending file; ', f)

        if verbose:
            print('found ', len(files), ' files')

    return files
