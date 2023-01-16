import subprocess
from utils.configs_values import user,server
from utils.exit_handlers import *

is_remote = True

def ssh_check():
    if not is_remote:
        return
    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0].decode() != 'ok\n':
        exit_error(f"Given {user=} and {server=} are not correct.")

def subprocess_result_check(subprocess_result):
    if subprocess_result[1].decode() == "":
        print_end(f"Done.")
    else:
        exit_error(subprocess_result[1].decode())

def subprocess_ssh_command(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE):
    if is_remote :
        cmd = f"echo y | ssh {user}@{server} {cmd}"
    subprocess_result = subprocess.Popen(
            cmd, 
            shell=True, stdout=stdout, 
            stderr=stderr
            ).communicate()
    return subprocess_result

def scp_formating(host_name,file):
    if machine_name == "" :
        return f"{file}"
    else :
        return f"{machine_name}:{file}"

def subprocess_scp_command(src,dest,file_src,file_dest,stdout=subprocess.PIPE,stderr=subprocess.PIPE):
    if not is_remote :
        return
    src = scp_formating(src,file_src)
    dest = scp_formating(dest,file_dest)
    cmd = f"echo y | scp {src} {dest}"
    subprocess_result = subprocess.Popen(
        f"echo y | scp {src} {dest}", 
        shell=True, stdout=stdout, 
        stderr=stderr
        ).communicate()
    return subprocess_result

def walt_image_clone(hub_name):
    cmd = f"walt image clone {hub_name}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)
        

def walt_node_run(title,node_name,cmd,stdout=subprocess.PIPE):
    print_title(f"{title} ...")
    run_cmd = f"walt node run {node_name} {cmd}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)


def transfer_local_to_server(file_title,file_src,file_dest):
    print_title(f"Transfering {file_title} to walt server ...")
    src = ""
    dest = f"{user}@{server}"
    subprocess_result = subprocess_scp_command(src,dest,file_src,file_dest)
    subprocess_result_check(subprocess_result)

def transfer_server_to_node(file_title,file_src,file_dest,node_name):
    print_title(f"Transfering {file_title} to {node_name} ...")
    cmd = f"walt node cp {file_src} {node_name}:{file_dest}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)


def transefer_node_to_server(file_title,file_src,file_dest,node_name):
    print_title(f"Transfering {file_title} from {node_name} to walt server ...")
    cmd = f"walt node cp {node_name}:{file_src} {file_dest}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)



def transfer_server_to_local(file_title,file_src,file_dest):
    print_title(f"Tranfering {file_title} from walt server to local machine ...")
    cmd = f"scp {user}@{server}:{file_src} {file_dest}"
    src = f"{user}@{server}"
    dest = ""
    subprocess_result = subprocess_scp_command(src,dest,file_src,file_dest)

def walt_node_boot(node_name,image):
    print_title(f"Remote booting {node_name} with {image}")
    cmd = f"walt node boot {node_name} {image}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)
