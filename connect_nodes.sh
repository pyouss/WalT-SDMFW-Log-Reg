#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./connect_nodes.sh"
    echo "	Connect remote nodes with each other"
    exit 1
fi

ssid="DMFW"

for((i=0;i<$num_nodes;i++));  
do
    name="node_"${i}
    node=$(get_config NODEINFO $name $node_list_path)
    echo "Connecting ${node} through wifi to access point"
    ssh $user@$server walt node run ${node} ./connect.sh ${ssid}
    ssh $user@$server walt node run ${node} \'ping -c 4 10.0.1.1\'
    end_of_command_message
done 
