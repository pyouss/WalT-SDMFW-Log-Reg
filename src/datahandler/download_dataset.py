import subprocess
import os
import sys
from utils.routes import ROOT_DIR

def runcmd(cmd, verbose = False, *args, **kwargs):
	process = subprocess.Popen(
		cmd,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE,
		text = True,
		shell = True
	)
	std_out, std_err = process.communicate()

	if verbose:
		print(std_out.strip(), std_err)
	pass

def download_dataset(args):

	if args["mnist"]:
		if not os.path.exists(f"{ROOT_DIR}/dataset"):
			os.makedirs("dataset")
		print("Downloading `sorted_mnist.csv` dataset ... (This might take time) ")
		runcmd("wget -O sorted_mnist.csv https://edge-intelligence.imag.fr/preprocessed_mnist_dataset/sorted_mnist.csv", verbose = False)
		runcmd("mv sorted_mnist.csv dataset/")
		print("You can find the dataset in : `{ROOT_DIR}/dataset/sorted_mnist.csv`")

	if args["cifar10"]:
		print("Downloading `sorted_cifar10.csv` dataset ... (This might take time) ")
		if not os.path.exists(f"{ROOT_DIR}/dataset"):
			os.makedirs("dataset")
		runcmd("wget -O sorted_cifar10.csv https://edge-intelligence.imag.fr/preprocessed_cifar10_dataset/sorted_cifar10.csv", verbose = False)
		runcmd("mv sorted_cifar10.csv dataset/")
		print(f"You can find the dataset in : `{ROOT_DIR}/dataset/sorted_cifar10.csv")