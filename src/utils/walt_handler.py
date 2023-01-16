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

def subprocess_result_check(subprocess_result,special_case=False,special_case_msg = ""):
    if subprocess_result[1].decode() == "":
        print_end()
    else:
        exit_error(subprocess_result[1].decode(),special_case,special_case_msg)

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
        return None
    src = scp_formating(src,file_src)
    dest = scp_formating(dest,file_dest)
    cmd = f"echo y | scp {src} {dest}"
    subprocess_result = subprocess.Popen(
        f"echo y | scp {src} {dest}", 
        shell=True, stdout=stdout, 
        stderr=stderr
        ).communicate()
    return subprocess_result

def walt_image_clone(image_name,hub_name,force=False):
    print_title(f"Retrieve walt image {image_name} from the hub")    
    cmd = f"walt image clone {hub_name}"
    if force:
        cmd = f"{cmd} --force"
        print_clone_warning() 
    subprocess_result = subprocess_ssh_command(cmd)
    special_case_msg ="The image is already in your walt server."
    special_case_msg+="If you want to force clone the image use the following `./sys init clone force` "
    subprocess_result_check(subprocess_result,
        special_case = True, 
        special_case_msg= special_case_msg
        )
        

def walt_node_run(title,node_name,cmd,stdout=subprocess.PIPE):
    print_title(f"{title}")
    run_cmd = f"walt node run {node_name} {cmd}"
    subprocess_result = subprocess_ssh_command(run_cmd,stdout=stdout)
    return subprocess_result


def transfer_local_to_server(file_title,file_src,file_dest):
    print_title(f"Transfering {file_title} to walt server")
    src = ""
    dest = f"{user}@{server}"
    subprocess_result = subprocess_scp_command(src,dest,file_src,file_dest)
    subprocess_result_check(subprocess_result)

def transfer_server_to_node(file_title,file_src,file_dest,node_name):
    print_title(f"Transfering {file_title} to {node_name}")
    cmd = f"walt node cp {file_src} {node_name}:{file_dest}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)


def transefer_node_to_server(file_title,file_src,file_dest,node_name):
    print_title(f"Transfering {file_title} from {node_name} to walt server")
    cmd = f"walt node cp {node_name}:{file_src} {file_dest}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)



def transfer_server_to_local(file_title,file_src,file_dest):
    print_title(f"Tranfering {file_title} from walt server to local machine")
    cmd = f"scp {user}@{server}:{file_src} {file_dest}"
    src = f"{user}@{server}"
    dest = ""
    subprocess_result = subprocess_scp_command(src,dest,file_src,file_dest)

def walt_node_boot(node_name,image):
    print_title(f"Remote booting {node_name} with {image}")
    cmd = f"walt node boot {node_name} {image}"
    subprocess_result = subprocess_ssh_command(cmd)
    subprocess_result_check(subprocess_result)

def walt_node_connect(node_name):
    title = f"Connecting {node_name} through wifi to access point"
    subprocess_result = walt_node_run(title,node_name,"./connect.sh DMFW")
    subprocess_result_check(subprocess_result)

def walt_test_connection(node_name):
    title = f"Testing connection between {node_name} and wifi access point"
    subprocess_result = walt_node_run(title,node_name,"\\'ping -c 3 10.0.1.1\\'")
    print(f"{subprocess_result[0].decode()}")
    if subprocess_result[1].decode() != "":
        print(f"Error : A problem occured when pinging {node_name} to the router.")
    print_end("")

def walt_start_hostapd(center_node):
    title = f"Starting hostapd"
    cmd = f"./restart_hostapd.sh"
    subprocess_result = walt_node_run(title,"rpi3bp-468-A",cmd)
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")
    print_end()

def walt_start_rabbitmq(center_node):
    title = f"Starting rabbit mq service"
    cmd = f"./start_rabbit.sh"
    subprocess_result = walt_node_run(title,center_node,cmd)
    print(f"{subprocess_result[0].decode()}")
    print(f"{subprocess_result[1].decode()}")
    print_end()

def walt_mkdir(folder):
    cmd=f"mkdir {folder}"
    subprocess_ssh_command(cmd)
