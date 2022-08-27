
#!/bin/bash
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./clean_environment.sh"
    echo "	Kill the process which is running"
    exit 1
fi


for((i=0;i<$num_nodes;i++));
do
    name="node_"${i}
    node=$(get_config NODEINFO $name $node_list_path)
    echo "Clearing processes on ${node}"
    ssh $user@$server walt node run ${node} killall python3
    end_of_command_message
done
