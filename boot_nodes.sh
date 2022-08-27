#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./boot_node.sh"
    echo "	Boot remote nodes without center node"
    echo "./boot_node.sh a"
    echo "	Boot remote nodes with center node"
    exit 1
fi



if [[ $1 == "a" ]];then
    echo "Remote booting ${center_node} with ${rabbit_image}"
    ssh $user@$server walt node boot ${center_node} ${rabbit_image}
    echo "-------------------------------------"
fi


image=$(get_config IMAGECONF node_image $local_config_image)

for((i=0;i<$num_nodes;i++));  
do
    name="node_"${i}
    node=$(get_config NODEINFO $name $node_list_path)
    echo "Remote booting ${node} with ${image}"
    ssh $user@$server walt node boot ${node} ${image}  
    echo "-------------------------------------"
done
