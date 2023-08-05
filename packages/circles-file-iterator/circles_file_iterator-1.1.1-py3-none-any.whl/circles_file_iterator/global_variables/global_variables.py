import os

# CYVERSE PATH
cyverse_path_server_resources = '/iplant/home/noecarras/resources_file_iterator/'
cyverse_path_server_resources_default = '/iplant/home/noecarras/resources_file_iterator/default/'
cyverse_path_server_resources_user = '/iplant/home/noecarras/resources_file_iterator/user/'
cyverse_path_server_resources_test = '/iplant/home/noecarras/resources_file_iterator/test/'

# LOCAL CACHES
local_folder = 'test'

local_temp_folder = os.path.join(local_folder, 'temp_cache')
local_long_folder = os.path.join(local_folder, 'long_cache')

