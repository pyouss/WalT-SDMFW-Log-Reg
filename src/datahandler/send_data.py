import subprocess
import configparser as cp
from utils.routes import ROOT_DIR,DATASET_DIR,REMOTE_DIR
from utils.configs_values import *
import utils.walt_handler as wh

def send_data(args):

    wh.ssh_check()

    if args["mnist"]:
        dataset_name = "sorted_mnist.csv"
    elif args["cifar10"]:
        dataset_name = "sorted_cifar10.csv"
    
    local_dataset_path = f"{DATASET_DIR}/{dataset_name}"
    remote_dataset_path = f"{REMOTE_DIR}/dataset/{dataset_name}"
    node_dataset_path = f"/persist/{dataset_name}"
    wh.transfer_local_to_server(f"{dataset_name}",local_dataset_path,remote_dataset_path)
    for i in range(num_nodes):
        node_name = working_nodes[i]
        wh.transfer_server_to_node(f"{dataset_name}",remote_dataset_path,node_dataset_path,node_name)
