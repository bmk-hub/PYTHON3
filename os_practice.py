#!/usr/bin/env python3

import os

dir_path = "/home/bmk/python3"
file_name = "my_calendar.py"

file_path = os.path.join(dir_path, file_name)

if os.path.exists(file_path):
	print("This file exists in the python3 directory.")
else:
	print("This file does not exist in the python3 directory.")
entries = os.listdir("/home/bmk/python3")

for name in entries:
	if name.endswith(".py"):
		print("Python file:", name)	
	
	
	
	



