from utils.configs_values import *
import pandas as pd
import os
import numpy as np
from utils.routes import *


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def regret_path(i):
    path = f"{REGRET_DIR}/{graph_name}-nodes{num_nodes}-{dataname}-batch_size{batch_size}-T{T}-L{L}-r{r}-eta{eta}-eta_exp{eta_exp}-rho{rho}-rho_exp{rho_exp}/node{i}"
    return path

def result_path(i):
    path = f"{OUTPUTS_DIR}/{graph_name}-nodes{num_nodes}-{dataname}-batch_size{batch_size}-T{T}-L{L}-r{r}-eta{eta}-eta_exp{eta_exp}-rho{rho}-rho_exp{rho_exp}/node{i}"
    return path

def optimal_path():
    path = f"{OUTPUTS_DIR}/{dataname}-T{T}-L{L}-r{r}"
    return path


def create_new_regret_file_name(i,extension=".csv"):
    regret_path_node = regret_path(i)
    create_directory(regret_path_node)
    return f"{regret_path_node}/regret{extension}"
    
def save_regret_file(regret, i, regret_file_name):
    df_regret = pd.DataFrame(regret).T
    df_regret.to_csv(regret_file_name, index=False, header = False)    
    print(f"The regret of node {i}  is in the file: {regret_file_name}")

def get_latest_output(i,extension=".csv"):
    latest_result = f"{result_path(i)}/result{extension}"
    outputs_flat = pd.read_csv(latest_result, header=None).to_numpy()
    outputs = [ v.reshape(shape) for v in outputs_flat ]
    return np.array(outputs)
