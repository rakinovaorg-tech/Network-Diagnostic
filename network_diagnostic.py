import ipaddress
import socket
import subprocess

hostname = socket.gethostname()

s= socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address= s.getsockname()[0]
s.close()


def get_gateway():
    result=subprocess.run(
        ["ip","route"],
        capture_output=True,
        text=True
    )
    gateway=("Not Found")
    interface=("Not Found")

    for line in result.stdout.splitlines():
        if line.startswith("default"):
            gateway=line.split()[2]
            interface = line.split()[4]
            break
    return gateway,interface
gateway, interface = get_gateway()

def get_network():      
    result_ip = subprocess.run(
        ["ip","addr"],
        capture_output = True,
        text = True
    )
    for line in result_ip.stdout.splitlines():   
        if "inet " in line and "127.0.0.1" not in line:
            interface_ip = line.split()[1]
            network= ipaddress.ip_network(
                interface_ip,
                strict=False
            )
            return str(network)

    return "Not Found"
network= get_network()
      

print()
print("===============================")
print("    NETWORK DIAGNOSTIC TOOL     ")

print("================================")
print()
print("HOSTNAME :",hostname)
print("IP ADDRESS : ",ip_address)
print("GATEWAY : ",gateway)
print("INTERFACE : ",interface)
print("NETWORK : ",network)

def check_connection():
    result = subprocess.run(
        ["ping","-c","1","8.8.8.8"],
        capture_output=True,
        text=True
    )
    if result.returncode== 0:
        print("INTERNET: CONNECTED")
   
        for line in result.stdout.splitlines():
            if "time=" in  line:
                latency = line.split("time=")[1].split()[0]
                print("LATENCY :",latency)
                return   
    else:
        print("INTERNET NOT CONNECTED")
latency = check_connection()
print("================================")


