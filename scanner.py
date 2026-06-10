from concurrent.futures import ThreadPoolExecutor
import json
import csv
import ipaddress
import socket

subnet = "172.20.10.0/24"
ip = "google.com"
ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 3389, 5900, 8080, 8443]

def scan_port(ip, port):
    try:
        socket.create_connection((ip, port), timeout=1)
        print(ip, port, ":OPEN")
        return (ip, port, "OPEN")
    except:
        print(ip, port, ":CLOSED")
        return (ip, port, "CLOSED")

def discover_hosts(subnet):
    live_hosts = []
    for ip in ipaddress.ip_network(subnet).hosts():
        try:
            socket.create_connection((str(ip), 80), timeout=1)
            print(str(ip), "is UP")
            live_hosts.append(str(ip))
        except:
            pass
    return live_hosts

def save_results(results):
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved to results.json")

    with open("results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ip", "port", "state"])
        for row in results:
            writer.writerow(row)
    print("Saved to results.csv")

if __name__ == "__main__":
    print("IP:", ip)
    results = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in ports]
    for future in futures:
        results.append(future.result())
    save_results(results)
    discover_hosts(subnet)