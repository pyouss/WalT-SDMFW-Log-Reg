import os
import sys
from configparser import ConfigParser
import configparser as cp
import subprocess
from utils.routes import ROOT_DIR,REMOTE_DIR
from utils.configs_values import *
from utils.files_path import *
import utils.walt_handler as wh
from utils.exit_handlers import *

def get_result():
    
    node_result_path = "/persist/result.csv"
    remote_result_path =f"{REMOTE_DIR}/result/result.csv"
    for i in range(len(working_nodes)):
        folder = result_path(i)
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_title = "results"
        file_src = node_result_path
        file_dest = remote_result_path
        node_name = working_nodes[i]
        wh.transefer_node_to_server(file_title,file_src,file_dest,node_name)
        
    
        file_title = "results"
        file_src = remote_result_path
        file_dest = result_path(i)
        wh.transfer_server_to_local(file_title,file_src,file_dest)
        
        print_end()