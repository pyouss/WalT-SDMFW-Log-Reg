#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.lock import lock_modifications
from utils.routes import ROOT_DIR
from utils.configs_values import *

local_config_param = f"{ROOT_DIR}/config/param.conf"
remote_config_param = f"{ROOT_DIR}/config/param.conf"
node_config_param= "/persist/param.conf"

def send_config():

    print(f"Transfering parameters to walt server ...")
    subprocess_result = subprocess.Popen(
            f"echo y | scp {local_config_param} {user}@{server}:{remote_config_param}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
    #print(f"{subprocess_result[0].decode()}")
    #print(f"{subprocess_result[1].decode()}")
    print("Done.")
    print()

    for i in range(num_nodes):
        node_name = working_nodes[i]
        print(f"Transfering parameters to {node_name} ...")
        cmd = f"walt node cp {remote_config_param} {node_name}:{node_config_param}"
        subprocess_result = subprocess.Popen(
            f"echo y | ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        #print(f"{subprocess_result[0].decode()}")
        #print(f"{subprocess_result[1].decode()}")   
        print("Done.")
        print()

    print(f"Transfering number of nodes to rabbitmq node {center_node} ...")
    cmd = f"walt node cp {remote_config_param} {center_node}:{node_config_param}"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    #print(f"{subprocess_result[0].decode()}")
    #print(f"{subprocess_result[1].decode()}")
    print("Done.")
    print()

