#!/bin/bash 
source ./utils/read_config_files.sh

if [ $# -eq 0 ]
then
    echo "Starting hostapd"
    ssh $user@$server walt node run ${center_node} ./restart_hostapd.sh 
    echo "Done."
    echo "-------------------------------------"


    echo "Starting rabbit mq server"
    ssh $user@$server walt node run ${center_node} ./start_rabbit.sh 
    echo "Done."
    echo "-------------------------------------"
    exit 1
fi

echo "-------------------------------------"
echo "./start_rabbit_node.sh

This command acts on the special node acting as the broker 
and WiFi access point.point.

It starts the configured hostapd service 
(for WiFi access point) with IP address 10.0.1.1
and the rabbitMQ server. "
echo "-------------------------------------"
echo "This command does not take any argument."
