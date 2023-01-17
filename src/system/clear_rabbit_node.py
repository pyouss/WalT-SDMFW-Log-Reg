import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *
import utils.walt_handler as wh
from utils.exit_handlers import *

def clear_rabbit_node():

    title = f"Clearing queues on rabbit_node"
    cmd = "python3 delete.py"
    wh.walt_node_run(title,center_node,cmd)

    cmd = "python3 declare.py"
    wh.walt_node_run("",center_node,cmd)
    
    print_end()
