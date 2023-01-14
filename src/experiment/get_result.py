import os
import sys
from configparser import ConfigParser
import configparser as cp
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *
from utils.files_path import *

def get_result():
    
    node_result_path = "/persist/result.csv"
    remote_result_path ="result/result.csv"
    for i in range(len(working_nodes)):
        folder = result_path(i)
        if not os.path.exists(folder):
            os.makedirs(folder)
        print(f"Transfering results from {working_nodes[i]} to walt server...")
        cmd = f"walt node cp {working_nodes[i]}:{node_result_path} {remote_result_path}"
        subprocess_result = subprocess.Popen(
                f"ssh {user}@{server} {cmd}", 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        #print(subprocess_result[0].decode())
        #print(subprocess_result[1].decode())
        print("Done.")
        print()
        print(f"Tranfering results from walt server to local machine ...")
        cmd = f"scp {user}@{server}:{remote_result_path} {result_path(i)}"
        subprocess_result = subprocess.Popen(
                cmd, 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        #print(subprocess_result[0].decode())
        #print(subprocess_result[1].decode())
        print("Done.")
        print()