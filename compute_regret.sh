#!/bin/bash 
source ./utils/read_config_files.sh

if [[ $1 == "help" ]];then
    echo "./compute_regret.sh"
    echo "	Compute the regret according to the configs"
    exit 1
fi

python3 utils/compute_regret.py
