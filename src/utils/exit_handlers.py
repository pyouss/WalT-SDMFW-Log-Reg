import sys

def print_line(n):
	line = ""
	for _ in range(n):
		line+="-"
	print(line)

def print_end():
	print("Done.")
	print_line(15)

def exit_error(msg):
	print("Error :")
	print(msg)

def print_title(title):
	print(f"{title} ...")
