import os
import importlib
import configparser as cp  # import the ConfigParser module
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *
import utils.walt_handler as wh

def boot_nodes(args):

    if args["all"]:
        wh.walt_node_boot(center_node,rabbit_image)


    for node_name in working_nodes:
        wh.walt_node_boot(node_name,node_image)