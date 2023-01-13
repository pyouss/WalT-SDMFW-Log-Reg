import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR


def boot_nodes():
    envi_config = cp.ConfigParser()
    envi_config.read(f'{ROOT_DIR}/config/envi.conf')
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
    node_config.read(f'{ROOT_DIR}/config/node.conf')
    nodes = node_config['NODEINFO']
    center_node = nodes["rabbit_node"]
    working_nodes = [node for node in nodes if node[:4] == "node"]
    image_config = cp.ConfigParser()
    image_config.read(f'{ROOT_DIR}/config/image.conf')
    rabbit_image = image_config["IMAGECONF"]["rabbit_image"]
    node_image = image_config["IMAGECONF"]["node_image"]

    if len(sys.argv) == 2 and sys.argv[1] == "a":
        print(f"Remote booting {center_node} with {rabbit_image}")
        cmd = f"walt node boot {center_node} {rabbit_image}"
        subprocess_result = subprocess.Popen(
            f"echo y | ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        print(f"{subprocess_result[0].decode()}")
        print(f"{subprocess_result[1].decode()}")


    for node in working_nodes:
        node_name = nodes[node]
        print(f"Remote booting {node_name} with {node_image}")
        cmd = f"walt node boot {node_name} {node_image}"
        subprocess_result = subprocess.Popen(
            f"echo y | ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        print(f"{subprocess_result[0].decode()}")
        print(f"{subprocess_result[1].decode()}")