#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./launch_experiment.sh"
    echo "	Launch an experiment according to the graph configuration and param configuration"
    exit 1
fi


echo "Running experiment"

for((i=1;i<$[$num_nodes];i++));  
do
    name="node_"${i}
    logname=".exectime"${i}".log"
    node=$(get_config NODEINFO $name $node_list_path)
    echo "Launch ${node}"
    echo y | ssh $user@$server walt node run ${node} python3 node.py > ${logname} &
done
name="node_0"
logname=".exectime0.log"
node=$(get_config NODEINFO $name $node_list_path)
echo "Launch ${node}"
echo y | ssh $user@$server walt node run ${node} python3 node.py > ${logname}


echo "Done."
echo "-------------------------------------"
