#!/usr/bin/env python3

with open("scan_logs.txt", "w") as f:
	f.write("Scanning started ...:\n")
	f.write("Target ip: 10.0.2.15\n")
	f.write("Target port 22:\n")
	
with open("scan_logs.txt", "r") as f:
	contents = f.read()
	print("The contents of the file are:")
	print(contents)
	
with open("scan_logs.txt", "a") as f:
	f.write("New scan session...:\n")
	f.write("Target: 10.0.2.10\n")
	f.write("Target: 22\n")
	
with open("scan_logs.txt", "r") as f:
	contents = f.read()
	print("The new contents of the file are: ")
	print(contents)
	
with open("scan_logs.txt", "r") as src, open("targets.txt", "w") as dst:
	for line in src:
		ip = line.strip()
		if ip:
			dst.write(f"{433}:\n")
			
import os

path = "targets.txt"

try:
    if os.path.exists(path):
        with open(path, "r") as f:
            for line in f:
                print("Target:", line.strip())
    else:
        print("targets.txt does not exist.")
except PermissionError:
    print("You don't have permission to read this file.")
			
			
	
	
	
	


