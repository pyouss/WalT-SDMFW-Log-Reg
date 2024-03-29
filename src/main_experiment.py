#!/usr/bin/python3
"""
Usage:
    ./experiment
    ./experiment launch [options]
    ./experiment [options]
    ./configure -h

Options:
    --time                              Stores timing of operations.
    -h, --help                          Show this help message and exit.
"""
from utils.lock import unlock_modifications,is_locked
from experiment.compute_regret import run_compute_regret
from experiment.launch_experiment import launch_experiment
from experiment.get_result import get_result
from experiment.store_exec_time import store_exec_time
import utils.walt_handler as wh 
import docopt


wh.ssh_check()

if not is_locked():
    print("Your configurations are unlocked.")
    print("This indicates that your configurations might not be synchronized with the remote server.")
    print()
    print("The experiment launcher is blocked until you send the current configurations by using :")
    print("\t./configure sync")
    exit()


args = docopt.docopt(__doc__)

if args["launch"]:
    launch_experiment()

get_result()

run_compute_regret()

if args["--time"]:
    print("Storing time of computations")
    store_exec_time()

print()
unlock_modifications()