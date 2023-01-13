import os
import sys
import shutil
import numpy as np
from configparser import ConfigParser

#Read config files
graph_config = ConfigParser()
graph_config.read("config/graph.conf")
param_config = ConfigParser()
param_config.read("config/param.conf")
local_graph_config = ConfigParser()

graph_type = graph_config["GRAPHTYPE"]

graph_param = graph_config[graph_type["type"]+"PARAM"]

algoconfig = param_config["ALGOCONFIG"]

nb_nodes = 0


def complete_graph():
	global nb_nodes
	n0 = int(graph_param["n0"])
	nb_nodes = n0
	return np.ones((n0,n0)) - np.diag(np.ones(n0)) 

def grid_graph():
	global nb_nodes
	n0 = int(graph_param["n0"])
	n1 = int(graph_param["n1"])
	nb_nodes = n0*n1
	res = np.zeros((nb_nodes, nb_nodes))
	for i in range(nb_nodes-1):
		if i % n1 == n1-1:
		    res[i,i+n1] = 1
		elif i >= (n0-1)*n1:
		    res[i,i+1] = 1
		else:
		    res[i,i+1] = 1
		    res[i,i+n1] = 1
	for i in range(nb_nodes):
		for j in range(i):
		    res[i,j] = res[j,i]
	return res

def line_graph():
	global nb_nodes
	n0 = int(graph_param["n0"])
	nb_nodes = n0
	i = list(range(1,n0))+list(range(n0-1)) 
	j = list(range(n0-1))+list(range(1,n0))
	res = np.zeros((n0,n0))
	res[i,j] = 1
	return res

def cycle_graph():
	global nb_nodes
	n0 = int(graph_param["n0"])
	nb_nodes = n0
	res = np.zeros((nb_nodes, nb_nodes))
	res[0, 1] = 1
	res[0, n0-1] = 1
	res[n0-1, n0-2] = 1
	res[n0-1, 0] = 1
	for i in range(1, n0-1):
		res[i, i-1] = 1
		res[i, i+1] = 1
	return res

def create_local_graph_conf(G,i):
	n0 = int(graph_param["n0"])
	s = ""
	for j in range(n0):
		if(G[i,j] == 1):
			s += str(j)
			s += ","
	s = s[:-1]
	local_graph_config["MYID"] = {"my_id" : str(i)}
	local_graph_config["NEIGHBORS"] = {"neighbors" : s}
	local_graph_config.write(open("graphs/node_"+str(i)+".conf", 'w'))


graph_function_name = {"complete" : complete_graph, "grid": grid_graph, "line": line_graph, "cycle": cycle_graph}


def create_graph():
	G = graph_function_name[graph_param["name"]]()
	if (os.path.exists("./graphs")) :
		shutil.rmtree("./graphs")
	os.mkdir("./graphs")
	for i in range(nb_nodes):
		graph = create_local_graph_conf(G,i)               
