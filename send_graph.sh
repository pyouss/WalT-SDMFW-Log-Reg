
#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [ $# -eq 0 ]
then
    python3 ./utils/create_graph.py

    echo "Transfering graph config to walt server"
    echo scp $local_config_graph $user@$server:$remote_config_graph
    scp $local_config_graph $user@$server:$remote_config_graph
    end_of_command_message

    for((i=0;i<$num_nodes;i++));  
    do
        name="node_"${i}
        graph_name="graphs/node_${i}.conf"
        echo "Transfering graph to walt server"
        scp $graph_name $user@$server:$graph_name
        echo "Done."
        echo "-------------------------------------"
        node=$(get_config NODEINFO $name $node_list_path)
        echo "Transfering graph to ${node}"
        ssh $user@$server walt node cp ${graph_name} "${node}:/persist/my_id.conf"
        echo "Done."
        echo "-------------------------------------"
        #ssh $user@$server walt node cp $remote_config_graph ${node}:$node_config_graph
    done 
    exit 1
fi

echo "./send_graph.sh

This command creates a graph according to the 'config/graph.conf' file,
and then sends the graph topology to the working nodes."
echo "-------------------------------------"
echo "This command does not take any argument."
  
