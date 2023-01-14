from utils.routes import ROOT_DIR
from utils.configs_values import *
import pandas as pd
import numpy as np


path = f"{ROOT_DIR}/dataset/{dataset}"
data = pd.read_csv(path, header = None).to_numpy()
y_data = np.zeros(data.shape[0],dtype=int)
x_data = data[:,1:].T
y_data = data[:,0].astype('int64')