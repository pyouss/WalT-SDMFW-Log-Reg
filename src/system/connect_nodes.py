import docopt
import os
import importlib
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *
import utils.walt_handler as wh

def connect_nodes(args):
    ssid = "DMFW"
    for i in range(num_nodes):
        node_name = working_nodes[i]
        if not args["--no_connect"]:
            wh.walt_node_connect(node_name)
             
        if args["--test"]:
            wh.walt_test_connection(node_name)
            
    if not args["--test"] :
        print("It is recommended to test if the connections are established.")
        print("Use option `-t` to do the tests.")
        print("\tUsage : `./sys connect nodes --test`")
        print("In order to save time, if you only wish to test and not try to connect then use `-n` option.")
        print("\tUsage : `./sys connect nodes --test --no_connect`")
        print("Check `./connect_nodes.py -h` to see test options.")

