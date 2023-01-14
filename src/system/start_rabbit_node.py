import os
import importlib
import sys
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *

def start_rabbit_node():

    print(f"Starting hostapd")
    cmd = f"walt node run {center_node} ./restart_hostapd.sh"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")

    print(f"Starting rabbit mq server")
    cmd = f"walt node run {center_node} ./start_rabbit.sh"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")
