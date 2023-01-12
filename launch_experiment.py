#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
import threading

envi_config = cp.ConfigParser()
envi_config.read('config/envi.conf')
user = envi_config['ENVCONFIG']['user']
server = envi_config['ENVCONFIG']['server']

ssh_check = subprocess.Popen(
    f"ssh {user}@{server} echo ok", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()

if ssh_check[0] != b'ok\n':
    print(f"Given {user=} and {server=} are not correct.")
    exit()

node_config = cp.ConfigParser()
node_config.read('config/node.conf')
nodes = node_config['NODEINFO']
center_node = nodes["rabbit_node"]
working_nodes = [nodes[node] for node in nodes if node[:4] == "node"]

param_config = cp.ConfigParser()
param_config.read('config/param.conf')
num_nodes = int(param_config["ALGOCONFIG"]["num_nodes"])
if num_nodes > len(working_nodes):
    print(f"Error : The number of nodes parameter {num_nodes=} exceeds the number of working nodes available in `config/node.conf`.")
    exit()

subprocess.Popen(f"python3 ./utils/create_graph.py", shell=True)


local_config_param = "config/param.conf"
remote_config_param = "config/param.conf"
node_config_graph= "/persist/my_id.conf"


log_files = [open(f".exectime{i}.log","w") for i in range(num_nodes)]

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
    print(f"{subprocess_result[1].decode()}")
    print(i)
t = []
for i in range(num_nodes):
    t.append(threading.Thread(target=run_node, args=(i,)))
    t[i].start()
for i in range(num_nodes):
    t[i].join()

print("Done.")
