import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR

def clear_rabbit_node():
    envi_config = cp.ConfigParser()
    envi_config.read(f'{ROOT_DIR}/config/envi.conf')
    user = envi_config['ENVCONFIG']['user']
    server = envi_config['ENVCONFIG']['server']

    node_config = cp.ConfigParser()
    node_config.read(f'{ROOT_DIR}/config/node.conf')
    nodes = node_config['NODEINFO']
    center_node = nodes["rabbit_node"]

    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0] != b'ok\n':
        print(f"Given {user=} and {server=} are not correct.")
        exit()


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
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")
    print("Done.")
