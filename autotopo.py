import os
import re
import yaml
import networkx as nx
import matplotlib.pyplot as plt
from netmiko import ConnectHandler
from netmiko.exceptions import NetMikoTimeoutException, NetMikoAuthenticationException
from dotenv import load_dotenv

load_dotenv()

def load_devices(file_path):
    if not os.path.exists(file_path):
        return get_default_devices()

    with open(file_path, "r") as file:
        data = yaml.safe_load(file)

    if not data or "devices" not in data:
        return get_default_devices()

    return data["devices"]

def get_default_devices():
    return [
        {"name": "R1", "device_type": "cisco_ios", "host": "192.168.100.10"},
        {"name": "R2", "device_type": "cisco_ios", "host": "192.168.100.11"},
        {"name": "R3", "device_type": "cisco_ios", "host": "192.168.100.12"},
    ]

def get_mock_cdp(device_name):
    mock_data = {
        "R1": """
Device ID: R2
Interface: Gig0/0
Device ID: R3
Interface: Gig0/1
""",
        "R2": """
Device ID: R1
Interface: Gig0/1
""",
        "R3": """
Device ID: R1
Interface: Gig0/0
"""
    }
    return mock_data.get(device_name, "")

def get_cdp_neighbors(device):
    device_copy = device.copy()
    device_name = device_copy.pop("name")

    device_copy["username"] = os.getenv("NET_USERNAME", "labuser")
    device_copy["password"] = os.getenv("NET_PASSWORD", "labpassword")
    device_copy["secret"] = os.getenv("NET_SECRET", "labsecret")

    try:
        connection = ConnectHandler(**device_copy)
        connection.enable()
        output = connection.send_command("show cdp neighbors detail")
        connection.disconnect()
        return output
    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        return get_mock_cdp(device_name)
    except Exception:
        return get_mock_cdp(device_name)

def parse_cdp_output(local_device, output):
    neighbors = []
    device_ids = re.findall(r"Device ID:\s*(\S+)", output)

    for neighbor in device_ids:
        neighbors.append((local_device, neighbor))

    return neighbors

def build_topology(devices):
    graph = nx.Graph()

    for device in devices:
        local_name = device["name"]
        graph.add_node(local_name)

        output = get_cdp_neighbors(device)
        neighbors = parse_cdp_output(local_name, output)

        for src, dst in neighbors:
            graph.add_edge(src, dst)

    return graph

def draw_topology(graph):
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(graph, seed=42)

    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_size=3000,
        node_color="lightblue",
        font_size=12,
        font_weight="bold",
        edge_color="gray",
    )

    plt.title("AutoTopo - Network Topology Map")
    plt.savefig("topology.png")
    plt.show()

def main():
    devices = load_devices("devices.yaml")
    graph = build_topology(devices)
    draw_topology(graph)

if __name__ == "__main__":
    main()