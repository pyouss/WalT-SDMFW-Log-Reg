#!/bin/bash 
source ./utils/read_config_files.sh

if [[ $1 == "help" ]];then
    echo "./init.sh"
    echo "	Create necessary folders in the remote server and local environment"
    exit 1
fi


folder=("graphs" "dataset" "config" "result" "tmp" "node_program")


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

create_dir "optimals"


echo "Set up is ready to use."
