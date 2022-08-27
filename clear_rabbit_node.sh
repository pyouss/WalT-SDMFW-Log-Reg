#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./clean_environment.sh"
    echo "	Kill the process which is running"
    exit 1
fi


echo "Clearing queues on rabbit node"
echo y | ssh $user@$server walt node run ${center_node} python3 delete.py
echo y | ssh $user@$server walt node run ${center_node} python3 declare.py
end_of_command_message
