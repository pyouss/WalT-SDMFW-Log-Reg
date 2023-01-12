#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess


if len(sys.argv) == 5 and sys.argv[1].upper() == "U" and sys.argv[3].upper() == "S":
    user_changed = subprocess.call(
        f"python3 modify_config.py u {sys.argv[2]}", 
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        )
    server_changed = subprocess.call(
        f"python3 modify_config.py s {sys.argv[4]}", 
        shell=True,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        )


envi_config = cp.ConfigParser()
envi_config.read('config/envi.conf')
user = envi_config['ENVCONFIG']['user']
server = envi_config['ENVCONFIG']['server']


dependencies = ['scipy', 'configparser', 'numpy', 'pandas', 'matplotlib', 'unittest', 'mat73']

def check_and_install(dependencies):
    for package in dependencies:
        try:
            importlib.import_module(package)
            print(f'{package} is already installed.')
        except ImportError:
            install_package = input(f'{package} is not installed. Would you like to install it? (y/n)')
            if install_package.lower() == 'y':
                import subprocess
                subprocess.call(f'pip3 install {package}', shell=True)
            else:
                print(f'{package} is not installed.')
                exit()



check_and_install(dependencies)

folders = ["graphs","dataset","config","result","tmp","node_program"]

ssh_check = subprocess.Popen(
    f"ssh {user}@{server} echo ok", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()

if ssh_check[0] != b'ok\n':
    print(f"Given {user=} and {server=} are not correct.")
    exit()

for folder in folders:
    cmd=f"mkdir {folder}"
    subprocess_result = subprocess.Popen(
        f"ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if not os.path.exists(f"./{folder}"):
        os.makedirs(folder)


print("Set up is ready.")