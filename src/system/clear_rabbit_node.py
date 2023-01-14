import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *

def clear_rabbit_node():

    print(f"Clearing queues on rabbit_node")
    cmd = f"walt node run {center_node} python3 delete.py"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")

    cmd = f"walt node run {center_node} python3 declare.py"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    #print(f"{subprocess_result[0].decode()}")
    #print(f"{subprocess_result[1].decode()}")
    print("Done.")
