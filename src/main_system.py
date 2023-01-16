#!/usr/bin/python3

"""
Usage:
    ./sys init
    ./sys init clone force
    ./sys init <username> <servername>
    ./sys init <username> <servername>  clone force
    ./sys boot
    ./sys boot all
    ./sys connect ap
    ./sys connect nodes [options]
    ./sys clean queues
    ./sys download [mnist | cifar10]
    ./sys load [mnist | cifar10]
    ./sys -h

Options:
    -t, --test     Test if the connection is established by sending pings.
    --no_connect   Only test and do not try to connect nodes to the router.
    ap           Starts the hostapd and rabbitmq services.
    -h, --help     Show this help message and exit.
"""

import docopt
from system.init import init 
from system.connect_nodes import connect_nodes
from system.start_rabbit_node import start_rabbit_node
from system.clear_rabbit_node import clear_rabbit_node
from system.boot_nodes import boot_nodes
from datahandler.download_dataset import download_dataset
from datahandler.send_data import send_data

args = docopt.docopt(__doc__)

if args["init"]:
    init(args)

if args["boot"]:
    boot_nodes(args)

if args["connect"] and args["ap"]:
    start_rabbit_node()
elif args["connect"] and args["nodes"]:
    connect_nodes(args)

if args["clean"] and args["queues"]:
    clear_rabbit_node()

if args["download"]:
    download_dataset(args)

if args["load"]:
    send_data(args)
