import os
import sys
import shutil
import numpy as np
sys.path.append('..')
from configparser import ConfigParser

#Read config files
graph_config = ConfigParser()
graph_config.read("config/graph.conf")
param_config = ConfigParser()
param_config.read("config/param.conf")

graph_type = graph_config["GRAPHTYPE"]

graph_param = graph_config[graph_type["type"]+"PARAM"]

algoconfig = param_config["ALGOCONFIG"]

nb_nodes = 0


def complete_graph():
	global nb_nodes
	n = int(graph_param["n"])
	nb_nodes = n
	return np.ones((n,n)) - np.diag(np.ones(n)) 

def grid_graph():
	global nb_nodes
	n = int(graph_param["n"])
	m = int(graph_param["m"])
	nb_nodes = n*m
	res = np.zeros((nb_nodes, nb_nodes))
	for i in range(nb_nodes-1):
		if i % m == m-1:
		    res[i,i+m] = 1
		elif i >= (n-1)*m:
		    res[i,i+1] = 1
		else:
		    res[i,i+1] = 1
		    res[i,i+m] = 1
	for i in range(nb_nodes):
		for j in range(i):
		    res[i,j] = res[j,i]
	return res

def line_graph():
	global nb_nodes
	n = int(graph_param["n"])
	nb_nodes = n
	i = list(range(1,n))+list(range(n-1)) 
	j = list(range(n-1))+list(range(1,n))
	res = np.zeros((n,n))
	res[i,j] = 1
	return res

def cycle_graph():
	global nb_nodes
	n = int(graph_param["n"])
	nb_nodes = n
	res = np.zeros((nb_nodes, nb_nodes))
	res[0, 1] = 1
	res[0, n-1] = 1
	res[n-1, n-2] = 1
	res[n-1, 0] = 1
	for i in range(1, n-1):
		res[i, i-1] = 1
		res[i, i+1] = 1
	return res

def create_local_graph_conf(G,i):
	s = "[MYID]"+"\n"+"my_id = "
	n = G.shape[0]
	s = s + str(i)+"\n\n"+"[NEIGHBORS]"+"\n"+"neighbors = "
	for j in range(n):
		if(G[i,j] == 1):
			s += str(j)
			s += ","
	s = s[:-1]
	return s


graph_function_name = {"complete" : complete_graph, "grid": grid_graph, "line": line_graph, "cycle": cycle_graph}



if __name__ == "__main__":
	G = graph_function_name[graph_param["name"]]()
	if (os.path.exists("./graphs")) :
		shutil.rmtree("./graphs")
	os.mkdir("./graphs")
	for i in range(nb_nodes):
		graph = create_local_graph_conf(G,i)
		graph_name = "graphs/node_"+str(i)+".conf"
		with open(graph_name, 'w') as f:   
			f.write(graph)                
