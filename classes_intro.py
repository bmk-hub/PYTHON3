#! /usr/bin/env python3

class PortList:
    def __init__(self, ip, open_ports):
        self.ip = ip
        self.open_ports = open_ports   # e.g. [22, 80, 443]

    def has_port(self, port):
        # Does this machine have this port open?
        return port in self.open_ports

    def count_ports(self):
        # How many open ports does this machine have?
        return len(self.open_ports)


# --- using the class ---

target = PortList("10.0.2.5", [22, 80, 443])

print("Open ports:", target.open_ports)

print("Is 22 open?", target.has_port(22))
print("Is 21 open?", target.has_port(21))

num = target.count_ports()
print("Number of open ports:", num)

if target.has_port(22):
    print("Port 22 is open, try SSH brute-force…")
else:
    print("No SSH here.")



