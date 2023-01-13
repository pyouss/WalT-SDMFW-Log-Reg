import os
import importlib
import configparser as cp 
import sys
import subprocess
import docopt
from config.config import modify_walt_user,modify_walt_server,update_configs
from utils.routes import ROOT_DIR

def init(args):
    if args['<username>'] and args['<servername>']:
        modify_walt_user(args['<username>'])
        modify_walt_server(args['<servername>'])
        update_configs()


    envi_config = cp.ConfigParser()
    envi_config.read(f'{ROOT_DIR}/config/envi.conf')
    user = envi_config['ENVCONFIG']['user']
    server = envi_config['ENVCONFIG']['server']


    dependencies = sorted(['scipy', 'configparser', 'numpy', 'pandas', 'matplotlib', 'unittest', 'mat73', 'docopt'])

    def check_and_install(dependencies):
        for package in dependencies:
            try:
                importlib.import_module(package)
                print(f'{package} is already installed.')
            except ImportError:
                install_package = input(f'{package} is not installed. Would you like to install it? (y/n)')
                if install_package.lower() == 'y':
                    subprocess.call(f'pip3 install {package}', shell=True)
                else:
                    print(f'{package} is not installed.')
                    exit()


    print("Checking dependencies ...")
    check_and_install(dependencies)

    folders = ["graphs","dataset","config","result","tmp","node_program"]
    print()
    print("Checking if connection by ssh is working fine ...")
    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0] != b'ok\n':
        print(f"Error : {user=} and {server=} are not correct.")
        print(f"\tUse `./init.py -h` if you need help initializing your username and WalT server name.")
        exit()
    else: 
        print("ssh connection is checked.")
    print()
    print("Retrieve walt images from the hub ...")
    cmd = "walt image clone hub:youssefp/sdmfw-logistic-regression"
    subprocess_result = subprocess.Popen(
            f"ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
    print(subprocess_result[0].decode())
    print(subprocess_result[1].decode())
    cmd = "walt image clone hub:youssefp/rabbit-node:rpi"
    subprocess_result = subprocess.Popen(
            f"ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
    print(subprocess_result[0].decode())
    print(subprocess_result[1].decode())
    print()
    print("Create all the needed directories ...")
    for folder in folders:
        cmd=f"mkdir {folder}"
        subprocess_result = subprocess.Popen(
            f"ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()

        if not os.path.exists(f"{ROOT_DIR}/{folder}"):
            os.makedirs(folder)


    print("Set up is ready.")


