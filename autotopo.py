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
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data["devices"]


def get_mock_cdp(device_name):
    """Mock CDP output for demo mode"""
    mock_data = {
        "R1": """
Device ID: R2
Interface: Gig0/0,  Port ID (outgoing port): Gig0/1

Device ID: R3
Interface: Gig0/1,  Port ID (outgoing port): Gig0/0
""",
        "R2": """
Device ID: R1
Interface: Gig0/1,  Port ID (outgoing port): Gig0/0
""",
        "R3": """
Device ID: R1
Interface: Gig0/0,  Port ID (outgoing port): Gig0/1
"""
    }
    return mock_data.get(device_name, "")


def get_cdp_neighbors(device):
    device_copy = device.copy()
    device_name = device_copy.pop("name")

    device_copy["username"] = os.getenv("NET_USERNAME", "labuser")
    device_copy["password"] = os.getenv("NET_PASSWORD", "labpassword")
    device_copy["secret"] = os.getenv("NET_SECRET", "labsecret")

    print(f"\nConnecting to {device_name}...")

    try:
        connection = ConnectHandler(**device_copy)
        connection.enable()
        output = connection.send_command("show cdp neighbors detail")
        connection.disconnect()
        print(f"Connected to {device_name}")
        return output

    except (NetMikoTimeoutException, NetMikoAuthenticationException):
        print(f"⚠ Using mock CDP data for {device_name}")
        return get_mock_cdp(device_name)

    except Exception as e:
        print(f"⚠ Error with {device_name}: {str(e)}")
        return get_mock_cdp(device_name)


def parse_cdp_output(local_device, output):
    neighbors = []

    device_ids = re.findall(r"Device ID:\s*(\S+)", output)
    interfaces = re.findall(r"Interface:\s*(\S+)", output)

    for i in range(min(len(device_ids), len(interfaces))):
        neighbors.append((local_device, device_ids[i]))

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
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=3000, node_color="lightblue",
            font_size=12, font_weight="bold", edge_color="gray")

    plt.title("AutoTopo - Network Topology Map")
    plt.savefig("topology.png")
    plt.show()
    print("\nTopology saved as topology.png")


def main():
    print("===== AutoTopo Network Discovery Started =====")
    devices = load_devices("devices.yaml")
    graph = build_topology(devices)
    draw_topology(graph)
    print("===== Topology Discovery Completed =====")


if __name__ == "__main__":
    main()