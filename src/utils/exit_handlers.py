import sys

def print_line(n):
	line = ""
	for _ in range(n):
		line+="-"
	print(line)

def print_end(msg = "Done."):
	print(msg)
	print_line(40)

def print_warning(msg):
	print("Warning : ")
	print(f"\t{msg}")

def exit_error(msg,special_case,special_case_msg):
	if not special_case:
		print("Error :")
		print(msg)
		sys.exit()
	print_end(special_case_msg)

def print_title(title):
	print(f"{title} ...")
	print()

def print_clone_warning():
	print("Warning : ")
	print("\tThis operation may reboot nodes. You need to prepare the environment again.")