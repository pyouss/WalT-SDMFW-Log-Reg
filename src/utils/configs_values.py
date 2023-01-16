import configparser as cp
from utils.routes import ROOT_DIR,CONFIG_DIR


envi_config = cp.ConfigParser()
envi_config.read(f'{CONFIG_DIR}/envi.conf')

graph_config = cp.ConfigParser()
graph_config.read(f'{CONFIG_DIR}/graph.conf')

param_config = cp.ConfigParser()
param_config.read(f'{CONFIG_DIR}/param.conf')

node_config = cp.ConfigParser()
node_config.read(f'{CONFIG_DIR}/node.conf')

image_config = cp.ConfigParser()
image_config.read(f'{CONFIG_DIR}/image.conf')



user = envi_config['ENVCONFIG']['user']
server = envi_config['ENVCONFIG']['server']



batch_size = param_config["ALGOCONFIG"]["batch_size"]
sub_batch_size = param_config["ALGOCONFIG"]["sub_batch_size"]
datainfo = param_config["DATAINFO"]
algoinfo = param_config["ALGOCONFIG"]
fwinfo = param_config["FWCONFIG"]

algoconfig = param_config["ALGOCONFIG"]
eta = float(algoinfo["eta"])
eta_exp = float(algoinfo["eta_exp"])
rho = float(algoinfo["rho"])
rho_exp = float(algoinfo["rho_exp"])
eta_fw = float(fwinfo["eta"])
eta_exp_fw = float(fwinfo["eta_exp"])
L_fw = int(fwinfo["l"])


#datainfo
dataset = datainfo["dataset"]
dataname = dataset.split(".", 1)[0]
f = int(datainfo["f"])   # number of features
c = int(datainfo["c"])   # number of classes
shape = (f,c)
dim = f*c

# Algorithm parameters
algoconfig = param_config["ALGOCONFIG"]
eta = float(algoinfo["eta"])
eta_exp = float(algoinfo["eta_exp"])
rho = float(algoinfo["rho"])
rho_exp = float(algoinfo["rho_exp"])
L = int(algoinfo["l"])

# Online dynamic
T = int(algoinfo["t"])
r = float(algoinfo["r"])
batch_size = int(algoinfo["batch_size"])
sub_batch_size = int(algoinfo["sub_batch_size"])

# FW configs
eta_fw = float(fwinfo["eta"])
eta_exp_fw = float(fwinfo["eta_exp"])
L_fw = int(fwinfo["l"])

# Graph configs
n0 = graph_config['COMPLETEPARAM']['n0']
num_nodes = int(algoinfo["num_nodes"])

graph_type = graph_config["GRAPHTYPE"]
graph_param = graph_config[graph_type["type"]+"PARAM"]



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

verified_type,graph_name = create_graph_name()

def checkInt(str):
    if str[0] in ('-', '+'):
        return str[1:].isdigit()
    return str.isdigit()

def grid_test(size, param):
    if int(size) != int(param[0]) * int(param[1]):
        print("Error : Size and parameter do not match")
        return False
    return True

def one_param_test(size,param):
    if len(param) == 1:
        if int(param[0]) == int(size):
            return True
        else :
            print("Error : Size and parameter do not match")
            return False    
    print("Error : Incorrect number of parameters")
    return False

special_graph_tests = {
'GRID': (grid_test,2), 
'COMPLETE':(one_param_test,1), 
'LINE': (one_param_test,1), 
'CYCLE':(one_param_test,1) }



# Nodes config
nodes = node_config['NODEINFO']
center_node = nodes["rabbit_node"]
working_nodes = [nodes[node] for node in nodes if node[:4] == "node"]
if num_nodes > len(working_nodes):
    print(f"Error : The number of nodes parameter {num_nodes=} exceeds the number of working nodes available in `config/node.conf`.")
    exit()

# Images config
rabbit_image = image_config["IMAGECONF"]["rabbit_image"]
node_image = image_config["IMAGECONF"]["node_image"]


def print_config_values():
    print(f"{dataname=}")
    print(f"{T=}")
    print(f"{L=}")
    print(f"{graph_name=}")
    decentralized_batch_size = int(batch_size/num_nodes)
    print(f"{decentralized_batch_size=}")