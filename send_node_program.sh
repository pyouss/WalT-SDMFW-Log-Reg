#!/bin/bash

local_config_envi="config/envi.conf"
node_list_path="config/node.conf"
local_config_param="config/param.conf"

function get_config(){
    sed -nr "/^\[$1\]/ { :l /^$2[ ]*=/ { s/[^=]*=[ ]*//; p; q;}; n; b l;}" $3
}


# Read config data from config.ini
user=$(get_config ENVCONFIG user $local_config_envi)
server=$(get_config ENVCONFIG server $local_config_envi)
num_nodes=$(get_config ALGOCONFIG num_nodes $local_config_param)

if [ $# -eq 0 ]
then
    scp node_program/test.py $user@$server:node_program/node.py

    for((i=0;i<$num_nodes;i++));
    do
        name="node_"${i}
        node=$(get_config NODEINFO $name $node_list_path)
        ssh $user@$server walt node cp node_program/node.py ${node}:node.py
    done
    exit 1
fi

echo "-------------------------------------"
echo "./send_node_program.sh

This command acts on the working nodes, the ones running SDMFW.

You can find a python script named 'node.py' in each of your working node.

If you feel the need to modify this script, you can do your modifications
in the script 'node.py' in the folder 'node_program'; 
then with this command you can send your modification to each of your working nodes."
echo "-------------------------------------"
echo "This command does not take any argument."
echo "-------------------------------------"
echo "It is important to note that if you reboot the nodes these modification will be lost."


