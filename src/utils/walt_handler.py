import subprocess
from utils.configs_values import user,server


def ssh_check():
    ssh_check = subprocess.Popen(
        f"ssh {user}@{server} echo ok", 
        shell=True, stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
        ).communicate()

    if ssh_check[0].decode() != 'ok\n':
        print(f"Given {user=} and {server=} are not correct.")
        exit()
