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
param = pika.ConnectionParameters('10.0.1.1','5672','/',credentials)
connection = pika.BlockingConnection(param)
channel = connection.channel()


# Variables and configurations


def read_config():
    """Reads the configuration file and returns the parsed data."""
    config = ConfigParser()
    try:
        config.read("/persist/my_id.conf")
    except ConfigParser.Error as e:
        print("Error reading config file: {}".format(e))
        return
    return config

def setup_variables(config):
    """Sets up the neighborhood_ids, my_neighbors_degree, and received_msg variables based on the data in the config file."""
    neighborhood_ids = {}
    my_neighbors_degree = {}
    received_msg = []
    my_degree = 0
    my_id_info = config["MYID"]
    my_id = my_id_info["my_id"]
    my_neighbors_info = config["NEIGHBORS"]
    my_neighbors = my_neighbors_info["neighbors"]
    my_neighbors = my_neighbors.split(',')
    for neighbor in my_neighbors:
        neighborhood_ids[neighbor] = my_degree
        received_msg.append(0)
        my_neighbors_degree[neighbor] = -1
        my_degree += 1
    received_msg_y = np.array(received_msg, dtype='int32')
    received_msg_d = np.array(received_msg, dtype='int32')
    my_degree = len(neighborhood_ids)
    return neighborhood_ids, my_neighbors_degree, received_msg, my_degree, my_id

def mux_degree(n_id, d, my_neighbors_degree):
    """Sets the degree of the specified neighbor in the my_neighbors_degree dictionary."""
    my_neighbors_degree[n_id] = d

def should_demux_degree(my_neighbors_degree):
    """Returns True if all values in the my_neighbors_degree dictionary are not -1, and False otherwise."""
    for d in my_neighbors_degree.values():
        if d == -1:
            return False
    return True

def demux_degree(my_degree, my_neighbors_degree, neighborhood_ids):
    """Calculates the weights for each neighbor in the neighborhood_ids dictionary."""
    weight = []
    for i in my_neighbors_degree:
        weight.append(1.0/(1 + max(int(my_degree), int(my_neighbors_degree[i]))))
    weight.append(1.0 - sum(weight))
    return weight

def send_degree(n, deg, channel):
    """Sends a message containing the current node's ID and degree to the specified neighbor."""
    msg = {
        'tag': 'degree',
        'id': my_id,
        'degree': str(deg),
    }
    channel.basic_publish(
        exchange=n,
        routing_key=n + '.notify',
        body=json.dumps({'tag': msg['tag'], 'degree': msg['degree'], 'id': my_id})
    )
    print("message sent")

def callback(ch, method, properties, body):
    """Handles messages received by the current node."""
    print("test")
    payload = json.loads(body)
    global weight
    print(f"I have received msg {n_id=} {deg=}")
    if payload.get('tag') == 'degree': 
        payload = json.loads(body)
        deg = payload.get('degree')
        n_id = payload.get('id')
        mux_degree(n_id, deg, my_neighbors_degree)
        print(f"I have received msg {n_id=} {deg=}")
        if should_demux_degree(my_neighbors_degree):
            ch.basic_ack(delivery_tag=method.delivery_tag)
            weight = demux_degree(my_degree, my_neighbors_degree, neighborhood_ids)
            channel.stop_consuming()
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)

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



def degree_exchange():
    """Exchanges the degrees of the current node and its neighbors."""
    msg = len(neighborhood_ids)
    for i in neighborhood_ids:
        print(f"{i=} {msg=}")
        send_degree(i, msg, channel)
    channel.basic_consume(on_message_callback=degree, queue=my_id+'_notify')
    channel.start_consuming()
    #channel.stop_consuming()

# Read the config file and set up the neighborhood_ids, my_neighbors_degree, and received_msg variables.
config = read_config()
neighborhood_ids, my_neighbors_degree, received_msg, my_degree, my_id = setup_variables(config)

weight = [0.0,0.0,0.0]

# Run the degree exchange process.
degree_exchange()
print(my_neighbors_degree)
exit()