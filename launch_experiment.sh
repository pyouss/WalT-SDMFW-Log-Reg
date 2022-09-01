#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./launch_experiment.sh"
    echo "	Launch an experiment according to the graph configuration and param configuration"
    exit 1
fi

if [[ $1 == "-t" ]];then
    rm .*.log 2> /dev/null
    for((i=0;i<$num_nodes;i++));  
    do
        name="node"${i}
        node_name="node_"${i}
        node=$(get_config NODEINFO $node_name $node_list_path)
        node_config_param="tmp/param_${node_name}.conf"
        echo "Retrieving parameters from node"
        #echo "ssh $user@$server walt node cp $node:/persist/param.conf $node_config_param" 
        ssh $user@$server walt node cp $node:/persist/param.conf $node_config_param
        scp $user@$server:$node_config_param $node_config_param
        diff -q -b -B $local_config_param $node_config_param > /dev/null
        echo $local_config_param $node_config_param
        if [[ $? != 0 ]]; then
            echo "Error ! Local node parameter different from remote node parameter. Please send param.conf"
            exit 1
        fi
        local_node_graph_conf="./graphs/$node_name.conf"
        remote_node_graph_conf="tmp/graph_${node_name}.conf"
        echo "Retrieving remote node graphs conf from node"
        echo "ssh $user@$server walt node cp $node:/persist/my_id.conf $remote_node_graph_conf"
        ssh $user@$server walt node cp $node:/persist/my_id.conf $remote_node_graph_conf
        scp $user@$server:$remote_node_graph_conf $remote_node_graph_conf
        diff -q -b -B $local_node_graph_conf $remote_node_graph_conf > /dev/null
        if [ $? != 0 ]; then
            echo "Error ! Local node graph different from remote node graph. Please send graphs"
            exit 1
        fi
    done
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
