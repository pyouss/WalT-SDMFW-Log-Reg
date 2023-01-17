import os
import importlib
import sys
import subprocess
import docopt
from config.config import modify_walt_user,modify_walt_server,update_configs
from utils.routes import ROOT_DIR,REMOTE_DIR
from utils.configs_values import *
import utils.walt_handler as wh
from utils.exit_handlers import *


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


def init(args):
    if args['<username>'] and args['<servername>']:
        modify_walt_user(args['<username>'])
        modify_walt_server(args['<servername>'])
        update_configs()

    print_title("Checking dependencies")
    check_and_install(dependencies)
    print_end()

    folders = ["graphs","dataset","config","result","tmp","node_program"]
    
    wh.ssh_check()
    
    print_title("Create all the needed directories")
    wh.walt_mkdir(f"{REMOTE_DIR}")
    for folder in folders:
        wh.walt_mkdir(f"{REMOTE_DIR}/{folder}")
        if not os.path.exists(f"{ROOT_DIR}/{folder}"):
            os.makedirs(folder)
    print_end()

    wh.walt_image_clone("sdmfw-logistic-regression","hub:youssefp/sdmfw-logistic-regression", force = args["force"])
    wh.walt_image_clone("rabbit-node:rpi","hub:youssefp/rabbit-node:rpi",force = args["force"])

    

    print_end("Set up is ready.")


