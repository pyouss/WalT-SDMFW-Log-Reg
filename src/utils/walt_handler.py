import subprocess
from utils.configs_values import user,server
from utils.exit_handlers import *


def ssh_check():
    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0].decode() != 'ok\n':
        exit_error(f"Given {user=} and {server=} are not correct.")
        

def walt_node_run(title,node_name,cmd,stdout=subprocess.PIPE):
    print_title(f"title ...")
    run_cmd = f"walt node run {node_name} {cmd}"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {run_cmd}", 
        shell=True, stdout=stdout, 
        stderr=subprocess.PIPE
        ).communicate()
    if subprocess_result[1].decode() == "":
        print_end(f"{node_name} done.")
    else:
        exit_error(subprocess_result[1].decode()[:-1])


def transfer_local_to_server(file_title,file):
    print_title(f"Transfering {file_title} to walt server ...")
    subprocess_result = subprocess.Popen(
        f"echo y | scp {file} {user}@{server}:{file}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    if subprocess_result[1].decode() == "":
        print_end(f"Done.")
    else:
        exit_error(subprocess_result[1].decode()[:-1])


def transfer_server_to_node(file_title,file,node_name):
    print(f"Transfering {file_title} to {node_name} ...")
    cmd = f"walt node cp {file} {node_name}:{file}"
    subprocess_result = subprocess.Popen(
        f"echo y | ssh {user}@{server} {cmd}", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()
    if subprocess_result[1].decode() == "":
        print_end(f"Done.")
    else:
        exit_error(subprocess_result[1].decode()[:-1])