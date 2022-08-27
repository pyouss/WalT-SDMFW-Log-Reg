1 Environment
	- python3.9
	- numpy
	- pandas
	- scipy

2 Execute
	Step 0: Create folders in remote server and local environment
		- "./init.sh"

	Step 1: Send data to nodes
		- Enter in dataset folder
		- "./load_mnist.sh" with argument to load dataset

	Step 2: Send graph to nodes
		- "./send_graph.sh"

	Step 3: Send configuration to nodes
		- "./send_config.sh"

	Step 4: Launch experiment
		- "./boot_nodes.sh"
		- "./start_rabbit_node.sh"
		- "./clear_rabbit_node.sh"
		- "./connect_nodes.sh"
		- "./launch_experiment.sh"

	Step 5: Getresult from nodes
		- "./get_result.sh"

	Step 6: Compute regret
		- "./compute_regret.sh"




