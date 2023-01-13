#!/usr/bin/python3

"""
Usage:
    ./modify_config.py [options]
    ./modify_config.py graph grid <height> <width>
    ./modify_config.py graph <graph_type> <size>
    ./modify_config.py mnist
    ./modify_config.py cifar10
    ./modify_config.py user <user> server <server>
    ./modify_config.py -h

Options:
    -l L                                Specify the number of iterations in an online round.
    -t T                                Specify the number of online rounds.
    --batch_size BATCH_SIZE             Specify the batch size.
    --sub_batch_size SUB_BATCH_SIZE     Specify the sub-batch size.
    -h, --help                          Show this help message and exit.
"""

import docopt
import sys
import configparser as cp



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
    print(f"Error :\n\t{msg}\nUse `./modify_config.py -h` to show the help options.")
    exit()

def no_arguments(args):
    for arg in args:
        if args[arg]:
            return False
    return True

def main():
    modified = False
    args = docopt.docopt(__doc__)
    if args['graph'] and args['grid']:
        graph_size = (int(args['<height>']), int(args['<width>']))
        modified = modify_graph(type="GRID", size=graph_size[0]*graph_size[1] ,
            param=sort_by_int([graph_size[0],graph_size[1]]))  
        update_configs()
        print(f"Graph type: grid {graph_size[0]}x{graph_size[1]}")
        print(f"Graph size: {graph_size[0]*graph_size[1]}")

    elif args['graph'] and args['<graph_type>'] != "grid":
        
        graph_type = args['<graph_type>']
        
        if graph_type not in [ "complete", "line", "cycle"] :
            err_msg = "Invalid graph type. Use 'grid', 'complete', 'line', or 'cycle'."
            exit_error(err_msg)
        
        graph_size = int(args['<size>'])
        
        modified = modify_graph(type=graph_type.upper(), size=graph_size ,param=[graph_size]) 
        update_configs()
        print("Graph type:", graph_type)
        print("Graph size:", graph_size)
    
    elif args['graph']:
        exit_error("Missing parameters : Grid graphs requires two integer parameters.")

    if args['-t']:
        print(f"T : {args['-t']}")
        modified = modify_round(T=args['-t'])
        update_configs()
    
    if args['-l']:
        print(f"L : {args['-l']}")
        modified = modify_iterations(T=args['-l'])
        update_configs()
    
    
    if args['--batch_size']:
        print("Batch size:", args['--batch_size'])
        print("Careful when choosing the sub_batch_size :\n")
        print("\tThe batch_size * T should be smaller or equal than the whole dataset size.")
        print("\tAlso, the sub_batch_size should be smaller or equal than batch_size.")
        modified = modify_batch_size(batch_size=args['batch_size'])
        update_configs()

    if args['--sub_batch_size']:
        print("Sub batch size:", args['--sub_batch_size'])
        print("Careful when choosing the sub_batch_size :\n")
        print("\tThe sub_batch_size should be smaller or equal than batch_size.") 
        modified = modify_sub_batch_size(sub_batch_size=args['--sub_batch_size'])
        update_configs()

    if args['mnist']:
        print("You switched the dataset of your experiment to `sorted_mnist.csv`.")
        print("Setting default configuration for MNIST dataset.")
        modified = modify_mnist()
        update_configs()

    if args['cifar10']:
        print("You switched the dataset of your experiment to `sorted_cifar10.csv`.")
        print("Setting default configuration for CIFAR10 dataset")
        modified = modify_cifar10()
        update_configs()

    if args['user'] and args['server']:
        print(f"User : {args['<user>']}")
        print(f"Server : {args['<server>']}")
        modified = modify_walt_user(user=args['<user>'])
        modified = modify_walt_server(server=args['<server>'])
        update_configs()

    if no_arguments(args):
        print("Use `./modify_config.py -h` to show the help options.")

    return modified

if __name__ == '__main__':
    if main():
        print("Done.")
        print("You can verify your updated configuration in files : `config/param.conf` `config/graph.conf` `config/envi.conf`")
