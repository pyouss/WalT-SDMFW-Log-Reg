import os
import sys
from configparser import ConfigParser
import configparser as cp
import subprocess
from utils.routes import ROOT_DIR
from utils.configs_values import *

def get_result():

    def str_int_float(iorf):
        if int(iorf) == iorf:
            return str(int(iorf))
        return str(iorf)

    def one_param_graph() :
            n0 = graph_param["n0"]
            return True,graph_param["name"]+str(n0)
        
    def two_param_graph():
        n0 = graph_param["n0"]
        n1 = graph_param["n1"]
        if n0 > n1:
            temp = n0
            n0 = n1
            n1 = temp
        return False,graph_param["name"]+str(n0)+"_"+str(n1)
        
    def error_graph():
        return False,"Error graph type"

    graph_function_name = {"complete" : one_param_graph, "grid": two_param_graph, "line": one_param_graph, "cycle": one_param_graph}
    create_graph_name = graph_function_name[graph_param["name"]]


    def result_path(i):
        verified_type,graph_name = create_graph_name()
        path = graph_name +"-"+"nodes"+str(num_nodes)+"-"+dataname+"-batch_size"+str(batch_size)+"-T"+str(T)+"-L"+str(L)+"-r"+str_int_float(r)+\
            "-eta"+str_int_float(eta)+"-eta_exp"+str_int_float(eta_exp)+"-rho"+str_int_float(rho)+"-rho_exp"+str_int_float(rho_exp)
        latest_result = f"{ROOT_DIR}/outputs/"+path+"/node"+str(i)
        return latest_result

    node_result_path = "/persist/result.csv"
    remote_result_path ="result/result.csv"
    for i in range(len(working_nodes)):
        folder = result_path(i)
        if not os.path.exists(folder):
            os.makedirs(folder)
        print(f"Transfering results from {working_nodes[i]} to walt server...")
        cmd = f"walt node cp {working_nodes[i]}:{node_result_path} {remote_result_path}"
        subprocess_result = subprocess.Popen(
                f"ssh {user}@{server} {cmd}", 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        #print(subprocess_result[0].decode())
        #print(subprocess_result[1].decode())
        print("Done.")
        print()
        print(f"Tranfering results from walt server to local machine ...")
        cmd = f"scp {user}@{server}:{remote_result_path} {result_path(i)}"
        subprocess_result = subprocess.Popen(
                cmd, 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        #print(subprocess_result[0].decode())
        #print(subprocess_result[1].decode())
        print("Done.")
        print()