import subprocess
import configparser as cp
from utils.routes import ROOT_DIR
from utils.configs_values import *


def send_data(args):

    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0] != b'ok\n':
        print(f"Given {user=} and {server=} are not correct.")
        exit()

    if args["mnist"]:
        dataset_name = "sorted_mnist.csv"
    elif args["cifar10"]:
        dataset_name = "sorted_cifar10.csv"
    
    local_dataset_path = f"{ROOT_DIR}/dataset/{dataset_name}"
    remote_dataset_path = f"dataset/{dataset_name}"
    node_dataset_path = f"/persist/dataset/{dataset_name}"

    print(f"Transfering parameters to walt server ...")
    subprocess_result = subprocess.Popen(
        f"echo y | scp {local_dataset_path} {user}@{server}:{remote_dataset_path}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    #print(f"{subprocess_result[0].decode()}")
    #print(f"{subprocess_result[1].decode()}")
    print("Done.")
    print()


    for i in range(num_nodes):
        node_name = working_nodes[i]
        print(f"Transfering datasets to {node_name} ...")
        cmd = f"walt node cp {remote_dataset_path} {node_name}:{node_dataset_path}"
        subprocess_result = subprocess.Popen(
            f"echo y | ssh {user}@{server} {cmd}", 
            shell=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
            ).communicate()
        #print(f"{subprocess_result[0].decode()}")
        #print(f"{subprocess_result[1].decode()}")   
        print("Done.")
        print()
