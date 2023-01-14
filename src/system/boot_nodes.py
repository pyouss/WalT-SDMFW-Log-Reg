import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR
from configs_values import *

def boot_nodes():

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