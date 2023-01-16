import subprocess
import configparser as cp
from utils.routes import ROOT_DIR,DATASET_DIR
from utils.configs_values import *
import utils.walt_handler as wh

def send_data(args):

    wh.ssh_check()

    if args["mnist"]:
        dataset_name = "sorted_mnist.csv"
    elif args["cifar10"]:
        dataset_name = "sorted_cifar10.csv"
    
    local_dataset_path = f"{DATASET_DIR}/{dataset_name}"
    remote_dataset_path = f"dataset/{dataset_name}"
    node_dataset_path = f"/persist/dataset/{dataset_name}"

    print(f"Transfering dataset to walt server ...")
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
        print(f"Transfering dataset to {node_name} ...")
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
