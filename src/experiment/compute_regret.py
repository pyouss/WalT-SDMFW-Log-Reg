import os
import sys
import json
import glob
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import figure, axes, title
from scipy.special import softmax
from configparser import ConfigParser
import utils.logistic_regression as log_r
from utils.configs_values import *
from utils.routes import *
from utils.files_path import *
from optimizers.fw import FW
from datahandler.read_data import * 


def loss_offline(x,t):
    return log_r.loss(x,x_data[:,:(t+1) * batch_size],y_data[:(t+1) * batch_size])

def loss_online(x,t):
    k = t * batch_size
    return log_r.loss(x,x_data[:,k:k + batch_size],y_data[k:k + batch_size])


def draw_regret(regret, name, title):
    figure(1, figsize=(10, 6))
    regret0 = [0.0] + regret
    x_axis = [i for i in range(T)]
    plt.plot(x_axis, regret0)
    title = title
    plt.title(title)
    plt.xlabel("Number of Rounds T")
    plt.ylabel("Regret")
    plt.savefig(name)
    plt.clf()


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


def run_compute_regret():
    
    start = time.time() 
    offline_optimal = compute_offline_optimal(100)
    
    for i in range(num_nodes):      
        online_output = []
        online_output = get_latest_output(i) 
        regret = []
        regret = compute_regret(online_output, offline_optimal,fixed=True)
        regret_file_name = create_new_regret_file_name(i)
        regret_plot_file_name = create_new_regret_file_name(i,extension="png") 
        print(regret)
        save_regret_file(regret, i, regret_plot_file_name)
        draw_regret(regret, f"{regret_plot_file_name}", f"Regret of node {i} in {graph_name}, {dataset=} {T=} {batch_size=} {L=}")        
        
        
    end = time.time()
    print(f"Time taken : {end - start}s")
    print()
    
        
        
        
