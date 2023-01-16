import os
import importlib
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *
import utils.walt_handler as wh

def start_rabbit_node():

    wh.walt_start_hostapd(center_node)
    wh.walt_start_rabbitmq(center_node)
