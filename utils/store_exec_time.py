import os
import sys
import shutil
import numpy as np
sys.path.append('..')
from configparser import ConfigParser


def exit_error(msg):
	print(f"Error : {msg}")
	exit()
		
def create_average_exec_time_file():
	exectime_log = []
	exectime_log.append(ConfigParser())
	exectime_log[0].read(".exectime0.log")

	num_nodes = exectime_log[0]["EXECTIME"]["num_nodes"]

	T = exectime_log[0]["EXECTIME"]["T"]
	L = exectime_log[0]["EXECTIME"]["L"]
	data_name = exectime_log[0]["EXECTIME"]["data_file"][10:]
	batch_size = exectime_log[0]["EXECTIME"]["batch_size"]
	for i in range(1,int(num_nodes)):
		
		exectime_log.append(ConfigParser())
		exectime_log[i].read(f".exectime{i}.log")
		if T != exectime_log[i]["EXECTIME"]["T"]:
			exit_error(f"Incoherents logs ! T is diferent in each file.")
		if L != exectime_log[i]["EXECTIME"]["L"]:
			exit_error(f"Incoherents logs ! L is diferent in each file.")
			
		if data_name != exectime_log[i]["EXECTIME"]["data_file"][10:]:
			exit_error(f"Incoherents logs ! data_name is diferent in each file.")
		if batch_size != exectime_log[i]["EXECTIME"]["batch_size"]:	
			exit_error(f"Incoherents logs ! batch_size is diferent in each file.")
	res = ConfigParser()
	T = int(T)
	L = int(L)
	batch_size = int(batch_size)
	num_nodes = int(num_nodes)
	time_of_rounds = [ float(e["EXECTIME"]["time_of_round"]) for e in exectime_log]
	time_of_data = [ float(e["EXECTIME"]["time_of_data"]) for e in exectime_log]
	time_of_comm = [ float(e["EXECTIME"]["time_of_comm"]) for e in exectime_log]
	time_of_iteration = [float(e["EXECTIME"]["time_of_iteration"]) for e in exectime_log]
	time_of_result = [float(e["EXECTIME"]["time_of_result"]) for e in exectime_log]
	overall = [float(e["EXECTIME"]["overall_time"]) for e in exectime_log]
	res["PARAM"] = { 
		'T' : str(T), 
		'L' : str(L), 
		'batch_size' : str(batch_size), 
		'data_name' : str(data_name),
		'num_nodes' : str(num_nodes)
	}
	res["AVERAGE"] ={
		"time_of_rounds" : str(sum(time_of_rounds)/num_nodes),
		"time_of_data" : str(sum(time_of_data)/num_nodes),
		"time_of_comm" : str(sum(time_of_comm)/num_nodes),
		"time_of_iteration" : str(sum(time_of_iteration)/num_nodes),
		"time_of_result" : str(sum(time_of_result)/num_nodes),
		"overall_time" : str(sum(overall)/num_nodes),
		"percentage_comm": str(sum(time_of_comm)/sum(overall)),
		"percentage_data": str(sum(time_of_data)/sum(overall)),
		"percentage_leftover" : str(1 - (sum(time_of_comm)+sum(time_of_data))/sum(overall))	
	}
	for i in range(num_nodes):
		res[f"NODE{i}"] = {
			"time_of_rounds" : str(time_of_rounds[i]),
			"time_of_data" : str(time_of_data[i]),
			"time_of_comm" : str(time_of_comm[i]),
			"time_of_iteration" : str(time_of_iteration[i]),
			"time_of_result" : str(time_of_result[i]),
			"overall_time" : str(overall[i]),
			"average_time_of_a_round" : str(time_of_rounds[i]/T),
			"average_time_of_a_data" : str(time_of_data[i]/T),
			"average_time_of_a_comm" : str(time_of_comm[i]/(T*L)),
			"average_time_of_an_iteration" : str(time_of_iteration[i]/(T*L))
		}
	files = os.listdir("exec_time_logs")
	i = max([0] + [int(f[8:-4])+1 for f in files]) 
	res.write(open(f"exec_time_logs/exectime{i}.log", 'w'))



if __name__ == "__main__":
	create_average_exec_time_file()