import os
import sys
import json
import glob
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import figure, axes, title
from unittest import result
from scipy.special import softmax
from configparser import ConfigParser
import logistic_regression as log_r
sys.path.append('..')

start = time.time()

pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 100000)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)



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


def str_int_float(iorf):
	if int(iorf) == iorf:
		return str(int(iorf))
	return str(iorf)

def one_param_graph() :
		n = graph_param["n"]
		return True,graph_param["name"]+str(n)
	
def two_param_graph():
	n = graph_param["n"]
	m = graph_param["m"]
	if n > m:
		temp = n
		n = m
		m = temp
	return False,graph_param["name"]+str(n)+"_"+str(m)
	
def error_graph():
	return False,"Error graph type"

graph_function_name = {"complete" : one_param_graph, "grid": two_param_graph, "line": one_param_graph, "cycle": one_param_graph}
create_graph_name = graph_function_name[graph_param["name"]]

nodes=[]
for i in range(num_nodes):
    section = "node_"+str(i)
    node_name = nodeinfo[section]
    nodes.append(node_name)


shape = (f,c)
x = np.ones(shape)
y = np.zeros(shape)
d = np.zeros(shape)
h = np.zeros(shape)
v = np.zeros(shape)


path = "dataset/"+dataset
data = pd.read_csv(path, header = None).to_numpy()
y_data = np.zeros(data.shape[0],dtype=int)
x_data = data[:,1:].T
y_data = data[:,0].astype('int64')

def loss_offline(x,t):
	return log_r.loss(x,x_data[:,:(t+1) * batch_size],y_data[:(t+1) * batch_size])

def loss_online(x,t):
	k = t * batch_size
	return log_r.loss(x,x_data[:,k:k + batch_size],y_data[k:k + batch_size])



def compute_gradient_offline(x,t):
	return log_r.compute_gradient(x,x_data[:,:(t+1)*batch_size],y_data[:(t+1)*batch_size])

def compute_gradient_online(x,t):
	k = t* batch_size
	j = k + batch_size
	return log_r.compute_gradient(x,x_data[:,k:j], y_data[k:j])


def update_x(x, v, eta_coef, eta_exp, t):
    eta = min(pow(eta_coef / (t + 1),eta_exp), 1.0)
    return x + eta*(v - x)

def FW(t):
	x = np.zeros(shape)
	for l in range(L_fw):
		gradient = compute_gradient_offline(x,t)
		v = log_r.lmo(gradient,r)		                
		x = update_x(x, v, eta_fw, eta_exp_fw, l)
	return x


def result_path():
	verified_type,graph_name = create_graph_name()

	path = graph_name +"-"+"nodes"+str(num_nodes)+"-"+dataname+"-batch_size"+str(decentralized_batch_size)+"-T"+str(T)+"-L"+str(L)+"-r"+str_int_float(r)+\
		"-eta"+str_int_float(eta)+"-eta_exp"+str_int_float(eta_exp)+"-rho"+str_int_float(rho)+"-rho_exp"+str_int_float(rho_exp)
	return path

def optimal_path():
	return "optimals/"+"nodes"+str(num_nodes)+"-"+dataname+"-batch_size"+str(batch_size)+"-T"+str(T)+"-L"+str(L)+"-r"+str(r)+".csv"

def draw_regret(regret, name):
	figure(1, figsize=(10, 6))
	x_axis = [i for i in range(1, T+1)]
	plt.scatter(x_axis, regret)
	title = result_path()
	plt.title(title)
	plt.xlabel("Number of Rounds T")
	plt.ylabel("Regret")
	plt.savefig(name)


def find_latest_result(node):
	out_path = "outputs/"+result_path()+"/" + node
	list_of_results = glob.glob(out_path+'/*') # * means all if need specific format then *.csv
	latest_result = max(list_of_results, key=os.path.getctime)
	return latest_result

def create_regret_directory(regret_path, node):
	if not os.path.exists(regret_path):
 		os.makedirs(regret_path)

def get_latest_output(i):
	node = "node"+str(i)
	latest_result = "outputs/" +result_path()+"/node"+str(i)+"/result.csv"
	outputs_flat = pd.read_csv(latest_result, header=None).to_numpy()
	outputs = [ v.reshape(shape) for v in outputs_flat]
	return np.array(outputs)

def create_new_regret_file_name(i):
	node = "node"+str(i)
	regret_path = "regrets/"+result_path()+"/"+node
	create_regret_directory(regret_path,node)
	return regret_path+"/regret"
	
def save_regret_file(regret, i, regret_file_name):
	df_regret = pd.DataFrame(regret).T
	df_regret.to_csv(regret_file_name+".csv", index=False, header = False)    
	print("The regret of node "+ str(i) +" is in the file: " + regret_file_name+".csv")




def compute_offline_optimal(t):
	#offline_optimal = pd.read_csv("dataset/optimal_lr.csv",header=None).to_numpy()
	offline_optimal = FW(t)
	return offline_optimal

def compute_regret(online_output,offline_optimal=None,fixed=False):
	if fixed :
		node_loss = [loss_online(online_output[t],t) -  loss_online(offline_optimal,t)  for t in range(T)]	
	else : 
		node_loss = [loss_online(online_output[t],t) - loss_online(compute_offline_optimal(t),t) for t in range(T)]
	regrets = np.cumsum(node_loss)
	return regrets


if __name__ == "__main__":
	start = time.time()	
	offline_optimal = compute_offline_optimal(100)
	
	for i in range(num_nodes):		
		online_output = get_latest_output(i)    	
		regret = compute_regret(online_output, offline_optimal,fixed=True)
		regret_file_name = create_new_regret_file_name(i)
		
		draw_regret(regret, regret_file_name+".png")		
		save_regret_file(regret, i, regret_file_name)
	    
	end = time.time()
	print("Time taken : " + str(end - start)+ "s")
	
	
	
	
	
