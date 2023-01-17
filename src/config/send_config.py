#!/usr/bin/python3

import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.lock import lock_modifications
from utils.routes import ROOT_DIR,CONFIG_DIR,GRAPH_DIR,REMOTE_DIR
from utils.configs_values import *
import utils.walt_handler as wh
from utils.create_graph import *

local_config_param = f"{CONFIG_DIR}/param.conf"
remote_config_param = f"{REMOTE_DIR}/config/param.conf"
node_config_param= "/persist/param.conf"
node_config_graph= "/persist/my_id.conf"

def send_config():
    
    wh.transfer_local_to_server("parameters",local_config_param,remote_config_param)
    
    wh.transfer_server_to_node("parameters",remote_config_param,node_config_param,center_node)

    for i in range(num_nodes):
        node_name = working_nodes[i]
        wh.transfer_server_to_node("parameters",remote_config_param,node_config_param,node_name)
    

def send_graph():

    create_graph()

    for i in range(num_nodes):
        node_name = working_nodes[i]
        local_graph_file_name = f"{GRAPH_DIR}/node_{i}.conf"
        graph_file_name = f"graphs/node_{i}.conf"
        remote_graph_file_name = f"{REMOTE_DIR}/graphs/node_{i}.conf"
        
        wh.transfer_local_to_server("graph topology",local_graph_file_name,remote_graph_file_name)

        node_name = working_nodes[i]
        wh.transfer_server_to_node("graph topology",remote_graph_file_name,node_config_graph,node_name)
        
