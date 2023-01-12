#!/bin/bash 
source ./utils/read_config_files.sh
source ./utils/pretyprint.sh

if [[ $1 == "help" ]];then
    echo "./get_result.sh"
    echo "	Get the results calculated by remote node and sotre them in local file"
    exit 1
fi

f=$(get_config DATAINFO f $local_config_param)
c=$(get_config DATAINFO c $local_config_param)
dataset=$(get_config DATAINFO dataset $local_config_param)
batch_size=$(get_config ALGOCONFIG batch_size $local_config_param)
L=$(get_config ALGOCONFIG l $local_config_param)
T=$(get_config ALGOCONFIG t $local_config_param)
eta=$(get_config ALGOCONFIG eta $local_config_param)
eta_exp=$(get_config ALGOCONFIG eta_exp $local_config_param)
rho=$(get_config ALGOCONFIG rho $local_config_param)
rho_exp=$(get_config ALGOCONFIG rho_exp $local_config_param)

r=$(get_config ALGOCONFIG r $local_config_param)
graph_type=$(get_config GRAPHTYPE type $local_config_graph)
graph_name=$(get_config "${graph_type}PARAM" name $local_config_graph)



if [[ $1 == "-t" ]];then
    remote_graph_config="./tmp/graph.conf"
    scp $user@$server:$remote_config_graph $remote_graph_config 
    remote_graph_type=$(get_config GRAPHTYPE type $remote_graph_config)
    if [[ $remote_graph_type != $graph_type ]];then
        echo "Local graph type does not match with remote graph type."
        exit 1
    fi
    if [[ $remote_graph_type != "GRID" ]];then
        local_n=$(get_config "${graph_type}PARAM" n $local_config_graph)
        remote_n=$(get_config "${remote_graph_type}PARAM" n $remote_graph_config)
        if [[ $local_n != $remote_n ]];then
            echo "Local graph parameters does not match remote graph parameter"
            exit 1
        fi
    else
        local_n=$(get_config "${graph_type}PARAM" n $local_config_graph)
        remote_n=$(get_config "${remote_graph_type}PARAM" n $remote_graph_config)
        local_m=$(get_config "${graph_type}PARAM" m $local_config_graph)
        remote_m=$(get_config "${remote_graph_type}PARAM" m $remote_graph_config)
        if [[ $local_n != $remote_n || $local_m != $remote_m ]];then
            echo "Local graph parameters does not match remote graph parameter"
            exit 1
        fi
    fi

    for((i=0;i<$num_nodes;i++));
    do
        name="node"${i}
        node_name="node_"${i}
        node=$(get_config NODEINFO $node_name $node_list_path)
        node_config_param="./tmp/param_${name}.conf"
        echo "Retrieving parameters from node"
        echo $user@$server walt node cp $node:/persist/param.conf $node_config_param
        ssh $user@$server walt node cp $node:/persist/param.conf $node_config_param
        echo scp $user@$server:$node_config_param $node_config_param
        scp $user@$server:$node_config_param $node_config_param
        end_of_command_message
        f_remote=$(get_config DATAINFO f $node_config_param)
        c_remote=$(get_config DATAINFO c $node_config_param)
        dataset_remote=$(get_config DATAINFO dataset $node_config_param)
        batch_size_remote=$(get_config ALGOCONFIG batch_size $local_config_param)
        L_remote=$(get_config ALGOCONFIG l $node_config_param)
        T_remote=$(get_config ALGOCONFIG t $node_config_param)
        eta_remote=$(get_config ALGOCONFIG eta $node_config_param)
        eta_exp_remote=$(get_config ALGOCONFIG eta_exp $node_config_param)
        rho_remote=$(get_config ALGOCONFIG rho $node_config_param)
        rho_exp_remote=$(get_config ALGOCONFIG rho_exp $node_config_param)
        r_remote=$(get_config ALGOCONFIG r $node_config_param)
        if [[ $f != $f_remote || $c != $c_remote || $dataset != $dataset_remote ]];then
            echo "Local node parameter [DATAINFO] does not match with nodes parameters."
            exit 1
        fi

        if [[ $batch_size != $batch_size_remote || $L != $L_remote || $T != $T_remote || $eta != $eta_remote || \
            $r != $r_remote || $eta_exp != $eta_exp_remote || $rho != $rho_remote || $rho_exp != $rho_exp_remote ]];then
            echo "Local node parameter [ALGOCONFIG] does not match with nodes parameters."
            exit 1
        fi
    done
fi

function create_name(){
    if [ "$graph_type" = "COMPLETE" ]
    then
        n=$(get_config COMPLETEPARAM n0 $local_config_graph)
        echo $graph_name$n
    elif [ "$graph_type" = "GRID" ]
    then
        n=$(get_config GRIDPARAM n0 $local_config_graph)
        m=$(get_config GRIDPARAM n1 $local_config_graph)
        if [ ${n} -gt ${m} ]; then
            temp=$n
            n=$m
            m=$temp
        fi
        echo $graph_name$n_$m
    elif [ "$graph_type" = "LINE" ]
    then
        n=$(get_config LINEPARAM n0 $local_config_graph)
        echo $graph_name$n
    elif [ "$graph_type" = "CYCLE" ]
    then
        n=$(get_config CYCLEPARAM n0 $local_config_graph)
        echo $graph_name$n
    else
        echo "Error type"
    fi
}



dataset_name=${dataset%.*}

# If name of dir does not exist, create dir
function create_dir(){
    dirname=$1
    if [ ! -d $dirname  ];then
    mkdir $dirname
    fi
}


function get_result(){
    local_result_path="$1/result.csv"
    #if [ -f $local_result_path  ];then
    #local_result_path="$1/result"`ls $1/result* | wc -l`.csv
    #local_result_path="$1/result.csv"
    #fi
    echo "Transfering results from node to walt server."
    ssh $user@$server walt node cp $2:$node_result_path $remote_result_path
    #echo $user@$server walt node cp $2:$node_result_path $remote_result_path
    end_of_command_message
    echo "Transefering results from walt server to local machine."
    scp $user@$server:$remote_result_path $local_result_path 
    end_of_command_message
    echo "You can find the output in ${local_result_path}"
}



gr=$(create_name)
dir1="outputs"
create_dir ${dir1}
dir2="${dir1}/${gr}-nodes${num_nodes}-${dataset_name}-batch_size${batch_size}-T${T}-L${L}-r${r}-eta${eta}-eta_exp${eta_exp}-rho${rho}-rho_exp${rho_exp}"
create_dir ${dir2}


for((i=0;i<$num_nodes;i++));
do
    name="node"${i}
    node_name="node_"${i}
    node=$(get_config NODEINFO $node_name $node_list_path)
    dir3="${dir2}/${name}"
    create_dir ${dir3}
    get_result ${dir3} ${node}
done



