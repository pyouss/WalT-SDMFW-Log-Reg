#!/bin/bash

local_config_envi="../config/envi.conf"
node_list_path="../config/node.conf"
local_config_param="../config/param.conf"

function get_config(){
    sed -nr "/^\[$1\]/ { :l /^$2[ ]*=/ { s/[^=]*=[ ]*//; p; q;}; n; b l;}" $3
}

if [ $# -eq 0 ];then 
    echo Error : Argument missing.
    echo Arguments options = \[ mnist, cifar10 \]
    echo Example to send the preprocessed mnist run the following command : 
    echo "  ./send_data.sh mnist"
    echo To send the preprocessed cifar10 run the following command : 
    echo "  ./send_data.sh cifar10"
fi

data="none"

if [[ $1 == "mnist" ]];then
    data="sorted_mnist.csv"
fi

if [[ $1 == "cifar10" ]];then
    data="sorted_cifar10.csv"
fi

if [[ $data == "none" ]];then
    echo Error : Wrong argument.
    echo Arguments options = \[ mnist, cifar10 \]
    echo Example to send the preprocessed mnist run the following command : 
    echo "  ./send_data.sh mnist"
    echo To send the preprocessed cifar10 run the following command : 
    echo "  ./send_data.sh cifar10"
fi

# Read config data from config.ini
user=$(get_config ENVCONFIG user $local_config_envi)
server=$(get_config ENVCONFIG server $local_config_envi)
num_nodes=$(get_config ALGOCONFIG num_nodes $local_config_param)

scp $data $user@$server:dataset/$data

for((i=0;i<$num_nodes;i++));  
do
    name="node_"${i}   
    node=$(get_config NODEINFO $name $node_list_path)
    ssh $user@$server walt node cp dataset/$data ${node}:/persist/$data
done 
