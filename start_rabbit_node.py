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

ssh_check = subprocess.Popen(
    f"ssh {user}@{server} echo ok", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()

if ssh_check[0] != b'ok\n':
    print(f"Given {user=} and {server=} are not correct.")
    exit()


print(f"Starting hostapd")
cmd = f"walt node run {center_node} ./restart_hostapd.sh"
subprocess_result = subprocess.Popen(
    f"echo y | ssh {user}@{server} {cmd}", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()
print(f"{subprocess_result[0].decode()}")
print(f"{subprocess_result[1].decode()}")

print(f"Starting rabbit mq server")
cmd = f"walt node run {center_node} ./start_rabbit.sh"
subprocess_result = subprocess.Popen(
    f"echo y | ssh {user}@{server} {cmd}", 
    shell=True, stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE
    ).communicate()
print(f"{subprocess_result[0].decode()}")
print(f"{subprocess_result[1].decode()}")
