#!/usr/bin/env python 3

port = int(input("Enter a port number: "))

if port == 22:
	print("This is commonly SSH.")
elif port == 80 or port == 8080:
	print("This is commonly HTTP(web).")
elif port == 443:
	print("This is commonly HTTPS(secure web).")
elif port == 21:
	print("This is commonly FTP.")
elif port == 445:
	print("This might be SMB(windows file sharing).")
else:
	print("This is an uncommon or custom port!")	
