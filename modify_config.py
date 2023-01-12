#!/usr/bin/python3

import configparser as cp
import sys

param_config = cp.ConfigParser()
param_config.read('config/param.conf')

envi_config = cp.ConfigParser()
envi_config.read('config/envi.conf')

graph_config = cp.ConfigParser()
graph_config.read('config/graph.conf')
n0 = graph_config["COMPLETEPARAM"]["n0"]
T = param_config["ALGOCONFIG"]["t"]
L = param_config["ALGOCONFIG"]["l"]
batch_size = param_config["ALGOCONFIG"]["batch_size"]
sub_batch_size = param_config["ALGOCONFIG"]["sub_batch_size"]
user = envi_config["ENVCONFIG"]["user"]
server = envi_config["ENVCONFIG"]["server"]

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

def modify_graph(type="COMPLETE", size=n0 ,param=[n0]):
	type = type.upper()
	graph_config.set('GRAPHTYPE','type',type)
	if len(param) != len(graph_config[type+'PARAM'])-1:
		print("Error : number of parameter do not match")
	if special_graph_tests[type][0](size,param):
		param_config.set('ALGOCONFIG','num_nodes',str(size))
		for i in range(len(param)):
			graph_config.set(type+'PARAM','n'+str(i),str(param[i]))
	return True

def modify_round(T=T):
	param_config.set('ALGOCONFIG','t',str(T))
	return True

def modify_iterations(L=L):
	param_config.set('ALGOCONFIG','l',str(L))
	return True


def modify_batch_size(batch_size=batch_size):
	if int(sub_batch_size) > int(batch_size):
		return False
	param_config.set('ALGOCONFIG','batch_size',str(batch_size))
	return True

def modify_sub_batch_size(sub_batch_size=sub_batch_size):
	if int(sub_batch_size) > int(batch_size):
		return False
	param_config.set('ALGOCONFIG','sub_batch_size',str(sub_batch_size))
	return True

def modify_walt_user(user=user):
	envi_config.set('ENVCONFIG','user',str(user))
	return True

def modify_walt_server(server=server):
	envi_config.set('ENVCONFIG','server',str(server))
	return True

def modify_cifar10():
	param_config.set('DATAINFO','dataset','sorted_cifar10.csv')
	param_config.set('DATAINFO','f','3072')
	param_config.set('DATAINFO','c','10')
	param_config.set('ALGOCONFIG','r','32')
	param_config.set('ALGOCONFIG','batch_size','500')
	param_config.set('ALGOCONFIG','sub_batch_size','4')
	param_config.set('ALGOCONFIG','l','10')
	param_config.set('ALGOCONFIG','t','100')
	param_config.set('ALGOCONFIG','eta','0.1')
	param_config.set('ALGOCONFIG','eta_exp','0.1')
	param_config.set('ALGOCONFIG','rho','1')
	param_config.set('ALGOCONFIG','rho_exp','0.5')
	param_config.set('ALGOCONFIG','reg_coef','100')
	param_config.set('FWCONFIG','eta','0.25')
	param_config.set('FWCONFIG','eta_exp','1')
	param_config.set('FWCONFIG','l','50')
	return True

def modify_mnist():
	param_config.set('DATAINFO','dataset','sorted_mnist.csv')
	param_config.set('DATAINFO','f','784')
	param_config.set('DATAINFO','c','10')
	param_config.set('ALGOCONFIG','r','8')
	param_config.set('ALGOCONFIG','batch_size','600')
	param_config.set('ALGOCONFIG','sub_batch_size','600')
	param_config.set('ALGOCONFIG','l','10')
	param_config.set('ALGOCONFIG','t','100')
	param_config.set('ALGOCONFIG','eta','1')
	param_config.set('ALGOCONFIG','eta_exp','1')
	param_config.set('ALGOCONFIG','rho','4')
	param_config.set('ALGOCONFIG','rho_exp','0.5')
	param_config.set('ALGOCONFIG','reg_coef','20')
	param_config.set('FWCONFIG','eta','1.5')
	param_config.set('FWCONFIG','eta_exp','1.5')
	param_config.set('FWCONFIG','l','50')
	return True

def sort_by_int(l):
	tmp = [ int(e) for e in l ]
	tmp = sorted(tmp)
	res = [ str(e) for e in tmp ]
	return res

def update_configs():
	with open('config/graph.conf', 'w') as configfile:
   		graph_config.write(configfile)
	with open('config/param.conf', 'w') as configfile:
		param_config.write(configfile)
	with open('config/envi.conf', 'w') as configfile:
		envi_config.write(configfile)

def exit_success(succ):
	print(str(succ))
	exit()


def exit_error(msg):
	print("Error : "+msg)
	exit()

if __name__ == "__main__":
	argc = len(sys.argv)
	modified = False
			
	if argc > 3:
		if sys.argv[1].upper() == "G":
			for i in range(3,argc):
				if not checkInt(str(sys.argv[i])):
					exit_error("graph parameters should be integers")
	
			if special_graph_tests[sys.argv[2].upper()][1] == 1 and argc==4:
				modified = modify_graph(sys.argv[2].upper(), sys.argv[3], [sys.argv[3]])
	
			if argc > 4:
				modified = modify_graph(sys.argv[2].upper(), sys.argv[3], sort_by_int(sys.argv[4:]))
	
			if modified:
				update_configs()
				exit_success("The graph topology is modified.")
	
	if argc == 3:
		if sys.argv[1].upper() in {"USER","U"}:
			modified = modify_walt_user(str(sys.argv[2]))
			update_configs()
			exit_success("The user name is modified.")

		if sys.argv[1].upper() in {"SERVER","S"}:
			modified = modify_walt_server(str(sys.argv[2]))
			update_configs()
			exit_success("The server is modified.")

		if sys.argv[1].upper() == "T":
			if not checkInt(str(sys.argv[2])):
				exit_error("number of rounds T should be integer")
	
			modified = modify_round(sys.argv[2])
	
		if sys.argv[1].upper() == "L":
			if not checkInt(str(sys.argv[2])):
				exit_error("number of iterations L should be integer")
			
			modified = modify_iterations(sys.argv[2])
			
		if sys.argv[1].upper() == "BS" or sys.argv[1].upper() =="BATCH_SIZE":
			if not checkInt(str(sys.argv[2])):
				exit_error("the size of batch should be integer")
		
			modified = modify_batch_size(sys.argv[2])

		if sys.argv[1].upper() == "SBS" or sys.argv[1].upper() =="SUB_BATCH_SIZE":
			if not checkInt(str(sys.argv[2])):
				exit_error("the size of sub batch should be integer")
			modified = modify_sub_batch_size(sys.argv[2])
			if modified == False:
				exit_error("The sub batch size should be less than the batch size.")
		
		if modified :
			update_configs()
			exit_success("The parameters are modified.")
	
		exit_error("Incorrect argument.")

	
	if argc == 2:
		if sys.argv[1].upper() == "MNIST" :
			modified = modify_mnist()
	
		if sys.argv[1].upper() == "CIFAR10" :
			modified = modify_cifar10()
	
		if modified :
			update_configs()
			exit_success(f"The parameters are set to default values for {sys.argv[1].upper()} dataset.")
	
		exit_error("Incorrect argument.")
	
	exit_error("Not enough arguments !")
