from concurrent.futures import ThreadPoolExecutor


import socket

ip = "google.com"
ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 5900, 8080, 8443]
print("IP:",ip)





def scan_port(ip,port):
    
    try:
        socket.create_connection((ip,port) , timeout=1)
        print(port, ":OPEN")
    except:
        print(port, ":CLOSED")


with ThreadPoolExecutor (max_workers=100) as executor:
    for port in ports:
        executor.submit(scan_port, ip, port)