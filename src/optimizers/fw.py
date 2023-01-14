import numpy as np
import utils.logistic_regression as log_r
from utils.configs_values import *
from datahandler.read_data import *



def compute_gradient_offline(x,t):
    return log_r.compute_gradient(x,x_data[:,:(t+1)*batch_size],y_data[:(t+1)*batch_size])


def update_x(x, v, eta_coef, eta_exp, t):
    eta = min(pow(eta_coef / (t + 1),eta_exp), 1.0)
    return x + eta*(v - x)

def FW(t):
    x = np.zeros(shape)
    for l in range(L_fw):
        gradient = compute_gradient_offline(x,t)
        v = log_r.lmo(gradient,r)                       
        x = update_x(x, v, eta_fw, eta_exp_fw, l)
    return x


