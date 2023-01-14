#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.lock import lock_modifications
from utils.create_graph import create_graph 
from utils.routes import ROOT_DIR
from utils.configs_values import *

local_config_param = f"{ROOT_DIR}config/param.conf"
remote_config_param = "config/param.conf"
node_config_graph= "/persist/my_id.conf"

def send_graph():

    create_graph()

    for i in range(num_nodes):
        node_name = working_nodes[i]
        graph_file_name = f"graphs/node_{i}.conf"
        
        print(f"Transfering graph to walt server ...")
        subprocess_result = subprocess.Popen(
            f"echo y | scp {graph_file_name} {user}@{server}:{graph_file_name}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        print("Done.")
        print()
        #print(f"{subprocess_result[0].decode()}")
        #print(f"{subprocess_result[1].decode()}")

        print(f"Transfering graph to {node_name} ...")
        cmd = f"walt node cp {graph_file_name} {node_name}:{node_config_graph}"
        subprocess_result = subprocess.Popen(
            f"echo y | ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        print("Done.")
        print()
        #print(f"{subprocess_result[0].decode()}")
        #print(f"{subprocess_result[1].decode()}")   

