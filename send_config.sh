
#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./send_config.sh"
    echo "	After modifying param.conf file, we should use this command to send configuration"
    exit 1
fi



graph_type=$(get_config GRAPHTYPE type $local_config_graph)
graph_name=$(get_config GRAPHTYPE type $local_config_graph)


function compute_nb_nodes(){
    if [ "$graph_name" = "COMPLETE" ]
    then
        n=$(get_config COMPLETEPARAM n $local_config_graph)
        echo $n
    elif [ "$graph_name" = "GRID" ]
    then
        n=$(get_config GRIDPARAM n $local_config_graph)
        m=$(get_config GRIDPARAM m $local_config_graph)
        echo $[$n * $m]
    elif [ "$graph_name" = "LINE" ]     
    then
        n=$(get_config LINEPARAM n $local_config_graph)
        echo $n
    elif [ "$graph_name" = "CYCLE" ]     
    then
        n=$(get_config CYCLEPARAM n $local_config_graph)
        echo $n
    else
        echo "Error type"
    fi
}

if [ $# -eq 0 ]
then
    nb_nodes=$(compute_nb_nodes)


    if [ $nb_nodes != $num_nodes ]
    then
        echo "Error, num_nodes doesn't equal to total number of nodes"
        exit 1
    fi


    echo "Transfering parameters to walt server"
    echo $local_config_param $user@$server:$remote_config_param
    scp $local_config_param $user@$server:$remote_config_param
    end_of_command_message


    for((i=0;i<$num_nodes;i++));
    do
        name="node_"${i}
        node=$(get_config NODEINFO $name $node_list_path)
        echo "Transfering parameters to ${node}"
        ssh $user@$server walt node cp $remote_config_param ${node}:$node_config_param
        end_of_command_message
    done


    name=rabbit-node
    node=$(get_config NODEINFO "rabbit_node" $node_list_path)

    echo "Transfering number of nodes to rabbitmq node. ${node}"
    ssh $user@$server walt node cp $remote_config_param ${node}:$node_config_param
    end_of_command_message
    exit 1
fi


echo "-------------------------------------"
echo "./send_config.sh

The SDMFW algorithm takes parameters such as the number of online rounds, 
the number of iteration, the size of a time step, ... 
You can modify 'config/param.conf' to choose your parameters, 
and then with this command you send the parameters to the working nodes."


