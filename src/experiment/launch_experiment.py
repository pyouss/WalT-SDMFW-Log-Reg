import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
import threading
from utils.create_graph import create_graph
from utils.routes import ROOT_DIR,EXEC_DIR
from utils.configs_values import *


local_config_param = f"{ROOT_DIR}/config/param.conf"
remote_config_param = "config/param.conf"
node_config_graph= "/persist/my_id.conf"

log_files = [open(f"{EXEC_DIR}/.exectime{i}.log","w") for i in range(num_nodes)]

def run_node(i):
    node_name = working_nodes[i]
    graph_file_name = f"graphs/node_{i}.conf"
    print(f"Running node {node_name}.")
    cmd = f"walt node run {node_name} python3 node.py "
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=log_files[i], 
        stderr=subprocess.PIPE
        ).communicate()
    #print(f"{subprocess_result[1].decode()}")
    print(f"{node_name} done.")

def launch_experiment():
    t = []
    for i in range(num_nodes):
        t.append(threading.Thread(target=run_node, args=(i,)))
        t[i].start()
    for i in range(num_nodes):
        t[i].join()

    print()