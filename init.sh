#!/bin/bash 
source ./utils/read_config_files.sh

if [[ $1 == "help" ]];then
    echo "./init.sh"
    echo "	Create necessary folders in the remote server and local environment"
    exit 1
fi

if [[ $1 == "u" ]];then
    if [[ $3 == "s" ]];then
        trash=$(python3 utils/p_config.py u $2)
        trash=$(python3 utils/p_config.py s $4)
        less config/envi.conf
    else
        echo "Error of arguments"
        exit 1
    fi
fi

folder=("graphs" "dataset" "config" "result" "tmp" "node_program")

ssh -q $user@$server exit
connection_failed=$?
if [[ $connection_failed != 0 ]];then
    echo "connection failed! Incorrect username or server"
    exit 1
fi


for i in ${folder[*]}
do
	ssh $user@$server mkdir ${i} 2> /dev/null
done

function create_dir(){
    dirname=$1
    if [ ! -d $dirname  ];then
    mkdir $dirname
    fi
}

create_dir "tmp"

create_dir "regrets"

create_dir "outputs"

create_dir "graphs"

echo "Set up is ready to use."

exit 1