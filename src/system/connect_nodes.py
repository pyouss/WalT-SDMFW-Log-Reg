import docopt
import os
import importlib
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *

def connect_nodes(args):
    ssid = "DMFW"
    for i in range(num_nodes):
        node_name = working_nodes[i]
        if not args["--no_connect"]:
            print(f"Connecting {node_name} through wifi to access point ...")
            cmd = f"walt node run {node_name} ./connect.sh {ssid}"
            subprocess_result = subprocess.Popen(
                f"echo y | ssh {user}@{server} {cmd}", 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
            print(f"{subprocess_result[0].decode()}")
            if subprocess_result[1].decode() != "":
                    print(f"Error : A problem occured when trying to connect {node_name} to the router.")
            
        if args["--test"]:
            print(f"Testing if node {node_name} is indeed connected to the router ...")
            cmd = f"walt node run {node_name} \\'ping -c 3 10.0.1.1\\' "
            subprocess_result = subprocess.Popen(
                f"echo y | ssh {user}@{server} {cmd}", 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
            print(f"{subprocess_result[0].decode()}")
            if subprocess_result[1].decode() != "":
                print(f"Error : A problem occured when pinging {node_name} to the router.")
    if not args["--test"] :
        print("It is recommended to test if the connections are established.")
        print("Use option `-t` to do the tests.")
        print("\tUsage : `./sys connect nodes --test`")
        print("In order to save time, if you only wish to test and not try to connect then use `-n` option.")
        print("\tUsage : `./sys connect nodes --test --no_connect`")
        print("Check `./connect_nodes.py -h` to see test options.")

