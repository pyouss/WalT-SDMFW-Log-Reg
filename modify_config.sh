#!/bin/bash

res=$(python3 utils/p_config.py $@)

if [[ $res == "2" ]];then
	less config/graph.conf
	less config/param.conf
elif [[ $res == "1" ]];then
	less config/param.conf
elif [[ $res == "3" ]];then
	less config/envi.conf
else
	echo $res
fi
