import os
import sys
from configparser import ConfigParser
import configparser as cp
import subprocess
from utils.routes import ROOT_DIR

def get_result():
    envi_config = cp.ConfigParser()
    envi_config.read(f'{ROOT_DIR}/config/envi.conf')
    user = envi_config['ENVCONFIG']['user']
    server = envi_config['ENVCONFIG']['server']


    #Read config.ini file
    param_config = ConfigParser()
    param_config.read("config/param.conf")

    node_object = ConfigParser()
    node_object.read("config/node.conf")

    graph_config = ConfigParser()
    graph_config.read("config/graph.conf")

    #Get the password
    datainfo = param_config["DATAINFO"]
    algoinfo = param_config["ALGOCONFIG"]
    fwinfo = param_config["FWCONFIG"]
    nodeinfo = node_object["NODEINFO"]

    f = int(datainfo["f"])   # number of features
    dataset = datainfo["dataset"]
    c = int(datainfo["c"])   # number of classes
    decentralized_batch_size = int(algoinfo["batch_size"])
    L = int(algoinfo["l"])
    T = int(algoinfo["t"])
    r = float(algoinfo["r"])
    num_nodes = int(algoinfo["num_nodes"])
    dataname = dataset.split(".", 1)[0]
    dim = f*c
    batch_size =  decentralized_batch_size


    graph_type = graph_config["GRAPHTYPE"]

    graph_param = graph_config[graph_type["type"]+"PARAM"]

    algoconfig = param_config["ALGOCONFIG"]
    eta = float(algoinfo["eta"])
    eta_exp = float(algoinfo["eta_exp"])
    rho = float(algoinfo["rho"])
    rho_exp = float(algoinfo["rho_exp"])

    eta_fw = float(fwinfo["eta"])
    eta_exp_fw = float(fwinfo["eta_exp"])
    L_fw = int(fwinfo["l"])

    node_config = cp.ConfigParser()
    node_config.read(f'{ROOT_DIR}/config/node.conf')
    nodes = node_config['NODEINFO']
    center_node = nodes["rabbit_node"]
    working_nodes = [nodes[node] for node in nodes if node[:4] == "node"]
    if num_nodes > len(working_nodes):
        print(f"Error : The number of nodes parameter {num_nodes=} exceeds the number of working nodes available in `config/node.conf`.")
        exit()




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
        path = graph_name +"-"+"nodes"+str(num_nodes)+"-"+dataname+"-batch_size"+str(decentralized_batch_size)+"-T"+str(T)+"-L"+str(L)+"-r"+str_int_float(r)+\
            "-eta"+str_int_float(eta)+"-eta_exp"+str_int_float(eta_exp)+"-rho"+str_int_float(rho)+"-rho_exp"+str_int_float(rho_exp)
        latest_result = f"{ROOT_DIR}/outputs/"+path+"/node"+str(i)
        return latest_result

    node_result_path = "/persist/result.csv"
    remote_result_path ="result/result.csv"
    for i in range(len(working_nodes)):
        folder = result_path(i)
        if not os.path.exists(f"{ROOT_DIR}/{folder}"):
            os.makedirs(folder)
        print(f"Transfering results from {working_nodes[i]} to walt server...")
        cmd = f"walt node cp {working_nodes[i]}:{node_result_path} {remote_result_path}"
        subprocess_result = subprocess.Popen(
                f"ssh {user}@{server} {cmd}", 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        print(subprocess_result[0].decode())
        print(subprocess_result[1].decode())
        print(f"Tranfering results from walt server to local machine ...")
        cmd = f"scp {user}@{server}:{remote_result_path} {result_path(i)}"
        subprocess_result = subprocess.Popen(
                cmd, 
                shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate()
        print(subprocess_result[0].decode())
        print(subprocess_result[1].decode())