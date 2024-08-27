from flask import Flask, render_template, request, redirect, url_for
import socket
import os
import json

app = Flask(__name__)

def ping_icmp(host):
    """Ping a server to check if it's online using ICMP."""
    response = os.system(f"ping -c 1 -w 2 {host} > /dev/null 2>&1")
    return "UP" if response == 0 else "DOWN"

def ping_port(host, port, timeout=5):
    """Ping a specific port on a host to check if it's open."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "UP"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "DOWN"

def load_servers():
    """Load servers from a JSON file."""
    if os.path.exists('servers.json'):
        with open('servers.json', 'r') as file:
            return json.load(file)
    return {}

def save_servers(servers):
    """Save servers to a JSON file."""
    with open('servers.json', 'w') as file:
        json.dump(servers, file, indent=4)

@app.route('/')
def index():
    servers = load_servers()

    # Check server and service statuses
    for server, details in servers.items():
        ip = details["ip"]
        server_status = ping_icmp(ip)
        servers[server]["status"] = server_status

        # Check each service status
        for service_name, service_details in details["services"].items():
            service_ip = service_details["ip"]
            service_status = ping_port(service_ip, service_details["port"])
            servers[server]["services"][service_name]["status"] = service_status

    return render_template('index.html', servers=servers)

@app.route('/add_server', methods=['POST'])
def add_server():
    servers = load_servers()
    server_name = request.form['server_name']
    server_ip = request.form['server_ip']
    if server_name and server_ip:
        servers[server_name] = {
            "ip": server_ip,
            "services": {}
        }
        save_servers(servers)
    return redirect(url_for('index'))

@app.route('/remove_server/<server_name>', methods=['POST'])
def remove_server(server_name):
    servers = load_servers()
    if server_name in servers:
        del servers[server_name]
        save_servers(servers)
    return redirect(url_for('index'))

@app.route('/add_service', methods=['POST'])
def add_service():
    servers = load_servers()
    server_name = request.form['server_name']
    service_name = request.form['service_name']
    service_ip = request.form['service_ip']
    service_port = request.form['service_port']
    service_url = request.form['service_url']

    if server_name in servers:
        servers[server_name]['services'][service_name] = {
            "port": int(service_port),
            "url": service_url,
            "ip": service_ip,
            "status": "UNKNOWN"
        }
        save_servers(servers)
    return redirect(url_for('index'))

@app.route('/remove_service/<server_name>/<service_name>', methods=['POST'])
def remove_service(server_name, service_name):
    servers = load_servers()
    if server_name in servers and service_name in servers[server_name]['services']:
        del servers[server_name]['services'][service_name]
        save_servers(servers)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
