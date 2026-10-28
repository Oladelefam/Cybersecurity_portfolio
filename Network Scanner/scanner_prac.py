import socket
import ipaddress

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
ipversion = ipaddress.ip_address(ip)
print(f'Hostname: {hostname}')
print(f'IP: {ip} - {ipversion.version}')