import configparser as cp
from utils.routes import ROOT_DIR


envi_config = cp.ConfigParser()
envi_config.read(f'{ROOT_DIR}/config/envi.conf')

graph_config = cp.ConfigParser()
graph_config.read(f'{ROOT_DIR}/config/graph.conf')

param_config = cp.ConfigParser()
param_config.read(f'{ROOT_DIR}/config/param.conf')

node_config = cp.ConfigParser()
node_config.read(f'{ROOT_DIR}/config/node.conf')

n0 = graph_config["COMPLETEPARAM"]["n0"]

user = envi_config['ENVCONFIG']['user']
server = envi_config['ENVCONFIG']['server']



T = param_config["ALGOCONFIG"]["t"]
L = param_config["ALGOCONFIG"]["l"]
batch_size = param_config["ALGOCONFIG"]["batch_size"]
sub_batch_size = param_config["ALGOCONFIG"]["sub_batch_size"]
datainfo = param_config["DATAINFO"]
algoinfo = param_config["ALGOCONFIG"]
fwinfo = param_config["FWCONFIG"]

f = int(datainfo["f"])   # number of features
dataset = datainfo["dataset"]
c = int(datainfo["c"])   # number of classes
batch_size = int(algoinfo["batch_size"])
sub_batch_size = int(algoinfo["sub_batch_size"])
L = int(algoinfo["l"])
T = int(algoinfo["t"])
r = float(algoinfo["r"])
num_nodes = int(algoinfo["num_nodes"])
dataname = dataset.split(".", 1)[0]
dim = f*c


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






nodes = node_config['NODEINFO']
center_node = nodes["rabbit_node"]
working_nodes = [nodes[node] for node in nodes if node[:4] == "node"]
if num_nodes > len(working_nodes):
    print(f"Error : The number of nodes parameter {num_nodes=} exceeds the number of working nodes available in `config/node.conf`.")
    exit()

image_config = cp.ConfigParser()
image_config.read(f'{ROOT_DIR}/config/image.conf')
rabbit_image = image_config["IMAGECONF"]["rabbit_image"]
node_image = image_config["IMAGECONF"]["node_image"]



    