#!/usr/bin/python3
"""
Usage:
    ./experiment launch
    ./experiment [options]
    ./experiment time
    ./configure -h

Options:
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
    print("\t./configure send")
    exit()


args = docopt.docopt(__doc__)

launch_experiment()

get_result()

run_compute_regret()

if args["time"]:
	store_exec_time()

print()
unlock_modifications()