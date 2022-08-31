import os
import pika
import json
import time
import numpy as np
import pandas as pd

from scipy.special import softmax
from configparser import ConfigParser

start = time.time()

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
my_id = my_id_info["my_id"]
my_neighbors_info = id_config["NEIGHBORS"]
my_neighbors = my_neighbors_info["neighbors"]
my_neighbors = my_neighbors.split(',')
for neighbor in my_neighbors:
    neighborhood_ids[neighbor] = my_degree
    received_msg.append(0)
    my_neighbors_degree[neighbor] = -1
    my_degree += 1
received_msg = np.array(received_msg, dtype='int32')
my_degree = len(neighborhood_ids)
print(f"{my_id=} {my_degree=} {my_neighbors=} {my_neighbors_degree=} {neighborhood_ids=}")

#Read config file
config_object = ConfigParser()
config_object.read("/persist/param.conf")

#Get the password
datainfo = config_object["DATAINFO"]
algoinfo = config_object["ALGOCONFIG"]

f = int(datainfo["f"])   # number of features
dataset = datainfo["dataset"]
data_file = "/persist/"+dataset
c = int(datainfo["c"])   # number of classes
batch_size = int(algoinfo["batch_size"])
L = int(algoinfo["l"])
T = int(algoinfo["t"])
num_nodes = int(algoinfo["num_nodes"])
r = float(algoinfo["r"])
eta = float(algoinfo["eta"])
eta_exp = float(algoinfo["eta_exp"])
rho = float(algoinfo["rho"])
rho_exp = float(algoinfo["rho_exp"])

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
eta_l = 0

neighborhood = []


def mux_degree(n_id, d):
	if d == None:
		print("I got degree wrong")
		return
	my_neighbors_degree[n_id] = d


def should_demux_degree():
	for d in my_neighbors_degree.values():
		if d == -1 :
			return False
	return True

def demux_degree():
	print(my_neighbors_degree,my_degree)
	for i in my_neighbors_degree:
		weight[neighborhood_ids[i]] = 1.0/(1 + max(int(my_degree), int(my_neighbors_degree[i])))
	weight[-1] = 1.0 - np.sum(weight)


def mux(n_id,v):
	if v.any() == None:
		print("I got something wrong")
		return
	v_id = neighborhood_ids[n_id]
	count = received_msg[v_id]
	if count >= len(neighborhood):
		neighborhood.append(np.zeros(dim))
	neighborhood[count] = neighborhood[count] + v * weight[v_id]
	received_msg[v_id] += 1

def should_demux():
	for i in received_msg:
		if i == 0:
			return False
	return True

def demux():
	global neighborhood
	global received_msg
	res = neighborhood[0]
	neighborhood = neighborhood[1:]
	received_msg = received_msg - np.ones(my_degree,dtype='int32')
	return res

def send_degree(n, deg, channel):
	msg = {
		'id' : my_id,
		'degree' : str(deg),
	}
	channel.basic_publish(
		exchange = n,
		routing_key = n + '.notify',
		body = json.dumps({'degree':msg['degree'], 'id': my_id}),
			mandatory=True
			)
		


def degree(ch, method, properties, body):
	payload = json.loads(body)
	deg = payload.get('degree')
	n_id = payload.get('id')
	print("received degree",deg,n_id)
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


def send_message(n, message, channel):
	message_I,message_J,message_value = sparse_list_definition(message) 
	msg = {
		'id' : my_id,
		'msg_I' : message_I,
		'msg_J' : message_J,
		'msg_values' : message_value,
	}
	channel.basic_publish(
		exchange = n,
		routing_key = n + '.notify',
		body = json.dumps({'msg_I' : msg['msg_I'], 
			'msg_J' : msg['msg_J'] , 
			'msg_values' : msg['msg_values'] ,
			'id' : my_id}),
			mandatory = True
	)

def send_message_to_neighbours(msg):
	for i in neighborhood_ids:
		send_message(i,msg,channel)


def callback_update_fed_y(ch, method, properties, body):
	global y
	payload = json.loads(body)
	rec_I =  payload.get('msg_I')
	rec_J = payload.get('msg_J')
	rec_values = payload.get('msg_values')
	rec = np.zeros(shape)
	rec[rec_I,rec_J] = rec_values	
	n_id = payload.get('id')
	mux(n_id,rec)
	if should_demux() :
		y = demux() + x * weight[-1]
		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming()
		return
	ch.basic_ack(delivery_tag = method.delivery_tag)

def callback_update_fed_d(ch, method, properties, body):
	global d
	payload = json.loads(body)
	rec_I =  payload.get('msg_I')
	rec_J = payload.get('msg_J')
	rec_values = payload.get('msg_values')
	rec = np.zeros(shape)
	rec[rec_I,rec_J] = rec_values
	n_id = format(payload['id'])
	mux(n_id,rec)

	if should_demux() :
		d = demux() +  g * weight[-1]
		ch.basic_ack(delivery_tag = method.delivery_tag)
		channel.stop_consuming()
		return
	ch.basic_ack(delivery_tag = method.delivery_tag)

def update_y():
	channel.basic_consume(on_message_callback = callback_update_fed_y, queue=my_id+'_notify')	
	channel.start_consuming()
	channel.stop_consuming()

def update_d():
	channel.basic_consume(on_message_callback = callback_update_fed_d, queue=my_id+'_notify')	
	channel.start_consuming()
	channel.stop_consuming()


def compute_gradient(x):
	data_size = x_data.shape[1]
	z = x.T @ x_data
	tmp_exp = np.exp(z)
	tmp_denominator= np.sum(tmp_exp,axis=0)
	tmp_exp = tmp_exp / tmp_denominator
	tmp_exp[y_data,range(data_size)] = tmp_exp[y_data,range(data_size)] - 1
	return (x_data / data_size) @ tmp_exp.T


def lmo(o):
	res = np.zeros(o.shape)
	max_rows = np.argmax(np.abs(o), axis=0)
	values = -r * np.sign(o[max_rows,range(o.shape[1])])
	res[max_rows, range(o.shape[1])] = values
	return res


def degree_exchange():
	msg = len(neighborhood_ids)
	for i in neighborhood_ids:
		print(f"{my_id=} ->  {i=} :  {msg=}")
		send_degree(i,msg,channel)
	channel.basic_consume(on_message_callback = degree, queue=my_id+'_notify')
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
	reg = 20 
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

	for t in range(T):
		x = np.zeros(shape)
		xs[0] = np.zeros(shape)
		for l in range(L):
			eta_l = min(eta / pow(l+1, eta_exp), 1.0)
			v = lmo(noise(o[l]))
			send_message_to_neighbours(xs[l])
			update_y()
			xs[l+1] = y + eta_l * (v - y)
			x = xs[l+1]
			print(f"{t=} {l=} x updates")

		x_data, y_data = receive_batch(t)
		result.append(xs[L].reshape(f*c))

		g = compute_gradient(xs[0])
		h = g
		for l in range(L):
			#rho_l = pow((2/(l+1)),(2/3)),
			send_message_to_neighbours(g)
			update_d()
			#a = rho_l * (d - a) + a 
			tmp = compute_gradient(xs[l+1])
			g = (tmp - h) + d
			h = tmp
			o[l+1] = o[l] + d
			print(f"{t=} {l=} g updates")
	pd.DataFrame(result).to_csv("/persist/result.csv", index=False, header = False)
	print("ok")

if (os.path.exists("/persist/result.csv")) :
	os.remove("/persist/result.csv")

degree_exchange()

DMFW()

print("node_"+str(my_id)+" done !")


end = time.time()
print("Time taken: " + str(end - start)+ "s")
exit()