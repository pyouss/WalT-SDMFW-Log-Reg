import os
import pika
import json
import time
import numpy as np
import pandas as pd

from scipy.special import softmax
from configparser import ConfigParser



np.set_printoptions(threshold = np.inf) 
np.set_printoptions(suppress = True)

credentials = pika.PlainCredentials('admin','password')
param = pika.ConnectionParameters('10.0.1.1','5672','/',credentials, heartbeat=600,
                                       blocked_connection_timeout=300)
connection = pika.BlockingConnection(param)
channel = connection.channel()


# Variables and configurations

id_config = ConfigParser()
id_config.read("/persist/my_id.conf")
neighborhood_ids = {}
my_neighbors_degree = {}
received_msg = []
my_degree = 0
my_id_info = id_config["MYID"]
print("[GAPHINFO]")
my_id = my_id_info["my_id"]
print(f"{my_id=}")
my_neighbors_info = id_config["NEIGHBORS"]
my_neighbors = my_neighbors_info["neighbors"]
print(f"{my_neighbors=}")
my_neighbors = my_neighbors.split(',')
for neighbor in my_neighbors:
    neighborhood_ids[neighbor] = my_degree
    received_msg.append(0)
    my_neighbors_degree[neighbor] = -1
    my_degree += 1
received_msg_y = np.array(received_msg, dtype='int32')
received_msg_d = np.array(received_msg, dtype='int32')
my_degree = len(neighborhood_ids)

#Read config file
config_object = ConfigParser()
config_object.read("/persist/param.conf")

datainfo = config_object["DATAINFO"]
print("[DATAINFO]")

f = int(datainfo["f"])   # number of features
dataset = datainfo["dataset"]
print(f"{dataset=}")
data_file = "/persist/"+dataset
c = int(datainfo["c"])   # number of classes
print(f"{c=}")
algoinfo = config_object["ALGOCONFIG"]
print("[ALGOCONFIG]")
batch_size = int(algoinfo["batch_size"])
print(f"{batch_size=}")
sub_batch_size = int(algoinfo["sub_batch_size"])
print(f"{sub_batch_size=}")
L = int(algoinfo["l"])
print(f"{L=}")
T = int(algoinfo["t"])
print(f"{T=}")
num_nodes = int(algoinfo["num_nodes"])
print(f"{num_nodes=}")
r = float(algoinfo["r"])
print(f"{r=}")
eta = float(algoinfo["eta"])
print(f"{eta=}")
eta_exp = float(algoinfo["eta_exp"])
print(f"{eta_exp=}")
rho = float(algoinfo["rho"])
print(f"{rho=}")
rho_exp = float(algoinfo["rho_exp"])
print(f"{rho_exp=}")
reg = float(algoinfo["reg_coef"])
print(f"{reg=}")

dim = (f,c) # dimension of the output and messages
shape = (f,c)

x = np.ones(dim)
y = np.zeros(dim)
d = np.zeros(dim)
g = np.zeros(dim)
h = np.zeros(dim)
v = np.zeros(dim)
a = np.zeros(dim)
weight = np.zeros(my_degree+1)
o = [np.zeros(dim) for _ in range(L+1)]
x_data = np.zeros([f,batch_size])
y_data = np.zeros([batch_size])
n = batch_size
local_batch_size = int(batch_size/num_nodes)
local_sub_batch_size = int(sub_batch_size/num_nodes)
eta_l = 0

neighborhood_y = []
neighborhood_d = []



def mux_degree(n_id, d):
	my_neighbors_degree[n_id] = d


def should_demux_degree():
	for d in my_neighbors_degree.values():
		if d == -1 :
			return False
	return True

def demux_degree():
	for i in my_neighbors_degree:
		weight[neighborhood_ids[i]] = 1.0/(1 + max(int(my_degree), int(my_neighbors_degree[i])))
	weight[-1] = 1.0 - np.sum(weight)
	return weight


def mux_y(n_id,v):
	global weight
	global neighborhood_y
	global received_msg_y
	v_id = neighborhood_ids[n_id]
	count = received_msg_y[v_id]
	if count >= len(neighborhood_y):
		neighborhood_y.append(np.zeros(dim))
	neighborhood_y[count] = neighborhood_y[count] + v * weight[v_id]
	received_msg_y[v_id] += 1

def should_demux_y():
	global received_msg_y
	for i in received_msg_y:
		if i == 0:
			return False
	return True

def demux_y():
	global neighborhood_y
	global received_msg_y
	res = neighborhood_y[0]
	neighborhood_y = neighborhood_y[1:]
	received_msg_y = received_msg_y - np.ones(my_degree,dtype='int32')
	return res

def mux_d(n_id,v):
	global weight
	global neighborhood_d
	global received_msg_d
	v_id = neighborhood_ids[n_id]
	count = received_msg_d[v_id]
	if count >= len(neighborhood_d):
		neighborhood_d.append(np.zeros(dim))
	neighborhood_d[count] = neighborhood_d[count] + v * weight[v_id]
	received_msg_d[v_id] += 1

def should_demux_d():
	global received_msg_d
	for i in received_msg_d:
		if i == 0:
			return False
	return True

def demux_d():
	global neighborhood_d
	global received_msg_d
	res = neighborhood_d[0]
	neighborhood_d = neighborhood_d[1:]
	received_msg_d = received_msg_d - np.ones(my_degree,dtype='int32')
	return res

def send_degree(n, deg, channel):
	msg = {
		'tag' : 'degree',
		'id' : my_id,
		'degree' : str(deg),
	}
	channel.basic_publish(
		exchange = n,
		routing_key = n + '.notify',
		body = json.dumps({'tag':msg['tag'],'degree':msg['degree'], 'id': my_id}),
			mandatory=True
			)
		


def degree(ch, method, properties, body):
	payload = json.loads(body)
	deg = payload.get('degree')
	n_id = payload.get('id')
	mux_degree(n_id,deg)
	if should_demux_degree() :
		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming()
		weight = demux_degree()
		return
	ch.basic_ack(delivery_tag = method.delivery_tag)


def sparse_list_definition(M):
	non_zeros_of_M = M.nonzero()
	if(len(non_zeros_of_M[0]) == 0):
		return [0], [0], [0]
	I = non_zeros_of_M[0].tolist()
	J = non_zeros_of_M[1].tolist()
	values = M[I,J].tolist()
	return I, J, values


def send_message(n, message,tag, channel):
	message_I,message_J,message_value = sparse_list_definition(message) 
	msg = {
		'tag' : tag,
		'id' : my_id,
		'msg_I' : message_I,
		'msg_J' : message_J,
		'msg_values' : message_value,
	}
	channel.basic_publish(
		exchange = n,
		routing_key = n + '.notify',
		body = json.dumps({'tag' : msg['tag'],
			'msg_I' : msg['msg_I'], 
			'msg_J' : msg['msg_J'] , 
			'msg_values' : msg['msg_values'] ,
			'id' : my_id}),
			mandatory = True
	)

def send_message_to_neighbours(msg,tag):
	for i in neighborhood_ids:
		send_message(i,msg,tag,channel)

def callback(ch,method,properties,body):
	payload = json.loads(body)
	global weight
	if payload.get('tag')=='degree': 
		payload = json.loads(body)
		deg = payload.get('degree')
		n_id = payload.get('id')
		mux_degree(n_id,deg)
		
		if should_demux_degree() :
			ch.basic_ack(delivery_tag = method.delivery_tag)
			channel.stop_consuming()
			weight = demux_degree()
			return
		ch.basic_ack(delivery_tag = method.delivery_tag)
	elif payload.get('tag')=='y_vector':
		global y
		payload = json.loads(body)
		rec_I =  payload.get('msg_I')
		rec_J = payload.get('msg_J')
		rec_values = payload.get('msg_values')
		rec = np.zeros(shape)
		rec[rec_I,rec_J] = rec_values	
		n_id = payload.get('id')
		mux_y(n_id,rec)
		if should_demux_y() :
			y = demux_y() + x * weight[-1]
			ch.basic_ack(delivery_tag = method.delivery_tag)
			channel.stop_consuming()
			return
		ch.basic_ack(delivery_tag = method.delivery_tag)
	elif payload.get('tag')=='d_vector':
		global d
		payload = json.loads(body)
		rec_I =  payload.get('msg_I')
		rec_J = payload.get('msg_J')
		rec_values = payload.get('msg_values')
		rec = np.zeros(shape)
		rec[rec_I,rec_J] = rec_values
		n_id = format(payload['id'])
		mux_d(n_id,rec)
		if should_demux_d() :
			d = demux_d() +  g * weight[-1]
			ch.basic_ack(delivery_tag = method.delivery_tag)
			channel.stop_consuming()
			return
		ch.basic_ack(delivery_tag = method.delivery_tag)
		

def update_y():
	channel.basic_consume(on_message_callback = callback, queue=my_id+'_notify')	
	channel.start_consuming()
	channel.stop_consuming()

def update_d():
	channel.basic_consume(on_message_callback = callback, queue=my_id+'_notify')	
	channel.start_consuming()
	channel.stop_consuming()


def compute_exact_gradient(x):
	data_size = x_data.shape[1]
	z = x.T @ x_data
	tmp_exp = np.exp(z)
	tmp_denominator= np.sum(tmp_exp,axis=0)
	tmp_exp = tmp_exp / tmp_denominator
	tmp_exp[y_data,range(data_size)] = tmp_exp[y_data,range(data_size)] - 1
	return (x_data / data_size) @ tmp_exp.T

def compute_stoch_gradient(x,s=local_sub_batch_size):
	sub_batch = np.floor(np.random.rand(s)*local_batch_size).astype(int)
	x_stoch_data,y_stoch_data = x_data[:, sub_batch], y_data[sub_batch]
	data_size = x_stoch_data.shape[1]
	z = x.T @ x_stoch_data
	tmp_exp = np.exp(z)
	tmp_denominator= np.sum(tmp_exp,axis=0)
	tmp_exp = tmp_exp / tmp_denominator
	tmp_exp[y_stoch_data,range(data_size)] = tmp_exp[y_stoch_data,range(data_size)] - 1
	return (x_stoch_data / data_size) @ tmp_exp.T

compute_gradient_fns = {}
compute_gradient_fns[True] = compute_exact_gradient
compute_gradient_fns[False] = compute_stoch_gradient

compute_gradient = compute_gradient_fns[local_sub_batch_size == local_batch_size]

def lmo(o):
	res = np.zeros(o.shape)
	max_rows = np.argmax(np.abs(o), axis=0)
	values = -r * np.sign(o[max_rows,range(o.shape[1])])
	res[max_rows, range(o.shape[1])] = values
	return res


def degree_exchange():
	msg = len(neighborhood_ids)
	for i in neighborhood_ids:
		send_degree(i,msg,channel)
	channel.basic_consume(on_message_callback = callback, queue=my_id+'_notify')
	channel.start_consuming()
	channel.stop_consuming()


def receive_batch(t):
	sk = (t* batch_size) + int(my_id)* local_batch_size
	data = pd.read_csv(data_file, skiprows=sk, nrows = local_batch_size, header = None)
	data = data.to_numpy()
	y_data = data[:,0].astype('int64')
	x_data = data[:,1:].T

	return x_data, y_data

def receive_batch_old(t):
	data = pd.read_csv(f"{data_file[:-4]}_{t}_{my_id}.csv", header = None, compression="gzip")
	data = data.to_numpy()
	y_data = data[:,0].astype('int64')
	x_data = data[:,1:].T

	return x_data, y_data


def noise(o):
	global reg
	noise = -0.5 + np.random.rand(shape[0],shape[1])
	return reg * o + noise

def DMFW():
	global x
	global y
	global g 
	global d
	global h
	global a
	global x_data
	global y_data
	result = []
	xs = [np.zeros(dim) for _ in range(L+1)]
	time_of_round = 0
	time_of_iteration = 0 
	time_of_comm = 0
	time_of_update = 0
	time_of_data = 0
	time_of_result = 0
	overall_time = -time.time()
	for t in range(T):
		
		time_of_round -= time.time()
		
		x = np.zeros(shape)
		xs[0] = np.zeros(shape)
		for l in range(L):
			
			time_of_comm -= time.time()
			send_message_to_neighbours(xs[l],'y_vector')
			update_y()
			time_of_comm += time.time()

			time_of_iteration -= time.time()
			eta_l = min(eta / pow(l+1, eta_exp), 1.0)
			v = lmo(noise(o[l]))
			xs[l+1] = y + eta_l * (v - y)
			x = xs[l+1]
			time_of_iteration += time.time()

		time_of_round += time.time()
		
		time_of_data -= time.time() 
		x_data, y_data = receive_batch(t)
		time_of_data += time.time()

		time_of_result -= time.time()
		result.append(xs[L].reshape(f*c))
		time_of_result += time.time()

		time_of_round -= time.time()
		g = compute_gradient(xs[0])
		h = g
		for l in range(L):
			time_of_comm -= time.time()
			send_message_to_neighbours(g,'d_vector')
			update_d()
			time_of_comm += time.time()

			time_of_iteration -= time.time()
			rho_l = min(rho / pow(l+1,rho_exp), 1.0)
			tmp = compute_gradient(xs[l+1])
			g = (tmp - h) + d
			h = tmp
			a = (1-rho_l) * a + d
			o[l+1] = o[l] + d
			time_of_iteration += time.time()

		time_of_round += time.time()
	overall_time += time.time()

	time_of_round = time_of_round 
	time_of_comm = time_of_comm
	time_of_iteration = time_of_iteration
	
	time_of_result -= time.time()
	pd.DataFrame(result).to_csv("/persist/result.csv", index=False, header = False)
	time_of_result += time.time()
	
	print(f"[EXECTIME]")
	print(f"{T=}")
	print(f"{L=}")
	print(f"{data_file=}")
	print(f"{batch_size=}")
	print(f"{num_nodes=}")
	print(f"{time_of_round=}")
	print(f"{time_of_data=}")
	print(f"{time_of_comm=}")
	print(f"{time_of_iteration=}")
	print(f"{time_of_result=}")
	print(f"{overall_time=}")	

if (os.path.exists("/persist/result.csv")) :
	os.remove("/persist/result.csv")


degree_exchange()


start = time.time()

DMFW()

end = time.time()

exit()