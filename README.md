# WalT handler to run SDMFW on Decentralized Online Logistic Regression

Welcome to the WalT deployment platform command-line tools!

This repository is designed to help you manage a WalT deployment platform, which involves connecting a group of Raspberry Pi 3b+ devices (referred to as "nodes") to a server that hosts the WalT platform. One Raspberry Pi acts as a wifi router and a rabbitmq broker, emulating a graph topology for the communication of the nodes. The other nodes have an image that includes a decentralized online algorithm called Stochastic Decentralized Meta Frank Wolfe (SDMFW), which optimizes online multiclass logistic regression in a decentralized setting.

The command-line tools consist of three main commands: sys, configure, and experiment. These tools are used to perform various system and experiment-related tasks, and they are command-line interfaces. Please make sure you have the appropriate permissions before running the commands.

The sys command is used for setting up the hardware and software environment, such as initializing the access point, connecting the Raspberry Pi nodes, booting the system, and checking for library dependencies. It also offers options to download and load datasets like MNIST and CIFAR10.

The configure command is used for configuring the algorithm and the topology of the graph for the experiment. This command allows the user to configure different aspects of the system, such as the graph, dataset, user, server, and adding nodes. It also offers options to sync and unlock the system, as well as showing the current configuration.

The experiment command is used to run the experiments after the environment has been set up and the configuration has been chosen and synchronized.

In summary, this project uses the SDMFW algorithm to optimize multiclass logistic regression in a decentralized manner using the MNIST and CIFAR10 datasets on a cluster of Raspberry Pi devices. The project is deployed on the WalT platform and provides scripts for parametrizing, launching, and receiving results from the experiment, as well as computing the regret analysis.

# Usage
The tools can be run using the following commands:

## ./sys
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
### Options 

- `-t`, `--test` - Test if the connection is established by sending pings
- `--no_connect` - Only test and do not try to connect nodes to the router
- `ap` - Starts the hostapd and rabbitmq services

This tool is used to configure the experiment parameters and it's environment, please make sure you have access to your walt platform before running the commands.

Note: The dataset options available are mnist and cifar10, you can download and load the specific dataset.

## ./configure

- `./configure [options]` - Runs the configuration with specified options
- `./configure graph grid <height> <width>` - Creates a grid graph with specified height and width
- `./configure graph <graph_type> <size>` - Creates a graph of specified type and size
- `./configure mnist` - Configures the system to use the MNIST dataset
- `./configure cifar10` - Configures the system to use the CIFAR-10 dataset
- `./configure localhost` - Configures the system to use the localhost
- `./configure user <user> server <server>` - Configures the system to use a specific user and server
- `./configure add <node_name>` - Adds a node to the system
- `./configure sync` - Synchronizes the configurations with all the nodes.
- `./configure unlock` - Unlocks the system
- `./configure show` - Shows the current configuration
- `./configure -h or ./configure --help` - Show the help message and exit

### Options
- `-l L` - Specify the number of iterations in an online round
- `-t T` - Specify the number of online rounds
- `--batch_size BATCH_SIZE` - Specify the batch size
- `--sub_batch_size SUB_BATCH_SIZE` - Specify the sub-batch size

This tool is used to configure the experiment parameters and it's environment, please make sure you have access to your walt platform before running the commands.

The graph command is used to create a graph with the specified options, mnist and cifar10 commands are used to configure the system to use the specified datasets.

## ./experiment
Once experiment's environment is set and chose the desired configurations. Launch the experiment with the following command :

```bash
./experiment launch [options]
```

If you haven't synchronized the configurations with the nodes then this command will be blocked.

### Options
You can store an analysis of different time benchmarks using the option `--time` : 
```bash
./experiment launch --time
```
