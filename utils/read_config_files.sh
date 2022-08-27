#!/bin/bash

local_config_param=./config/param.conf
local_config_envi=./config/envi.conf
node_config_param=/persist/param.conf
remote_config_param=config/param.conf
node_list_path=./config/node.conf
node_result_path=/persist/result.csv
remote_result_path=result/result.csv
local_config_image=./config/image.conf
local_config_graph=./config/graph.conf
remote_config_graph=config/graph.conf
node_config_graph=/persist/graph.conf

function get_config(){
    sed -nr "/^\[$1\]/ { :l /^$2[ ]*=/ { s/[^=]*=[ ]*//; p; q;}; n; b l;}" $3
}


user=$(get_config ENVCONFIG user $local_config_envi)
server=$(get_config ENVCONFIG server $local_config_envi)
num_nodes=$(get_config ALGOCONFIG num_nodes $local_config_param)
rabbit_image=$(get_config IMAGECONF rabbit_image $local_config_image)
center_node=$(get_config NODEINFO rabbit_node $node_list_path)

