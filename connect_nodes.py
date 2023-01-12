#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess

envi_config = cp.ConfigParser()
envi_config.read('config/envi.conf')
user = envi_config['ENVCONFIG']['user']
server = envi_config['ENVCONFIG']['server']

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

ssh_check = subprocess.Popen(
    f"ssh {user}@{server} echo ok", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()

if ssh_check[0] != b'ok\n':
    print(f"Given {user=} and {server=} are not correct.")
    exit()

ssid = "DMFW"
for i in range(num_nodes):
    node_name = working_nodes[i]
    print(f"Connecting {node_name} through wifi to access point")
    cmd = f"walt node run {node_name} ./connect.sh {ssid}"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")
    cmd = f"walt node run {node_name} \\'ping -c 3 10.0.1.1\\' "
    print(cmd)
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")