# WalT handler to run SDMFW on Decentralized Online Logistic Regression

Welcome to the WalT deployment platform command-line tools!

This repository is designed to help you manage a WalT deployment platform, which involves connecting a group of Raspberry Pi 3b+ devices (referred to as "nodes") to a server that hosts the WalT platform. One Raspberry Pi acts as a wifi router and a rabbitmq broker, emulating a graph topology for the communication of the nodes. The other nodes have an image that includes a decentralized online algorithm called Stochastic Decentralized Meta Frank Wolfe (SDMFW), which optimizes online multiclass logistic regression in a decentralized setting.

The command-line tools consist of three main commands: sys, configure, and experiment. These tools are used to perform various system and experiment-related tasks, and they are command-line interfaces. Please make sure you have the appropriate permissions before running the commands.

The sys command is used for setting up the hardware and software environment, such as initializing the access point, connecting the Raspberry Pi nodes, booting the system, and checking for library dependencies. It also offers options to download and load datasets like MNIST and CIFAR10.

The configure command is used for configuring the algorithm and the topology of the graph for the experiment. This command allows the user to configure different aspects of the system, such as the graph, dataset, user, server, and adding nodes. It also offers options to sync and unlock the system, as well as showing the current configuration.

The experiment command is used to run the experiments after the environment has been set up and the configuration has been chosen and synchronized.

In summary, this project uses the SDMFW algorithm to optimize multiclass logistic regression in a decentralized manner using the MNIST and CIFAR10 datasets on a cluster of Raspberry Pi devices. The project is deployed on the WalT platform and provides scripts for parametrizing, launching, and receiving results from the experiment, as well as computing the regret analysis.

#Usage
The tools can be run using the following commands:

##sys
- `./sys init` - Initializes the system
- `./sys init clone force` - Initializes the system with a force clone
- `./sys init <username> <servername>` - Initializes the system with a specific username and servername
- `./sys init <username> <servername> clone force` - Initializes the system with a specific username and servername, and force
- `./sys boot` - Boots all the nodes with their corresponding images
- `./sys boot all` - Boots all the system
- `./sys connect ap` - Starts the access point and rabbitmq service
- `./sys connect nodes [options]` - Connects the nodes to the router (it is recommanded to use option `--test` to test if the connection is established.)
- `./sys clean queues` - Cleans the queues (to make sure that no messages are hanging)
- `./sys download [mnist | cifar10]` - Downloads the specified dataset
- `./sys load [mnist | cifar10]` - Loads the specified dataset
- `./sys -h or ./sys --help` - Show the help message and exit

