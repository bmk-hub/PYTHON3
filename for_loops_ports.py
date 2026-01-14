#!/usr/bin/env python3

ports = [21, 22, 80, 8080, 3306, 53]

for port in ports:
	if port < 1024:
		print(port, "is a low (well-known) port.")
	else:
		print(port, "is a high(registered or dynamic) port.")
		
