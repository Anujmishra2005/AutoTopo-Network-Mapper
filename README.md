# AutoTopo - Intelligent Network Topology Discovery Tool

## Overview

AutoTopo is a Python-based network automation tool designed to
automatically discover and visualize network topology using Cisco CDP
neighbor information.

The tool connects to network devices via SSH, retrieves neighbor data,
parses interconnections, and generates a graphical topology map.

It supports both real lab environments and mock simulation mode for safe
public demonstrations.

------------------------------------------------------------------------

## Problem Statement

In enterprise environments:

-   Network topology documentation becomes outdated
-   Manual diagram creation is time-consuming
-   Troubleshooting is delayed due to unclear device relationships
-   Network visibility is limited

AutoTopo solves this by dynamically discovering device interconnections
and generating a visual network topology map.

------------------------------------------------------------------------

## Key Features

-   Automated CDP-based topology discovery
-   SSH connectivity using Netmiko
-   Multi-device support via YAML inventory
-   Graph-based topology modeling using NetworkX
-   Automatic topology visualization (PNG output)
-   Fault-tolerant design with mock fallback mode
-   Secure credential handling using environment variables
-   Privacy-safe public demonstration capability

------------------------------------------------------------------------

## Architecture Flow

1.  Load device inventory from YAML
2.  Establish SSH connection to each device
3.  Execute `show cdp neighbors detail`
4.  Parse neighbor relationships
5.  Construct graph model
6.  Generate topology visualization

------------------------------------------------------------------------

## Installation

Install required dependencies:

pip install netmiko pyyaml python-dotenv networkx matplotlib

------------------------------------------------------------------------

## Configuration

### devices.yaml

devices: - name: R1 device_type: cisco_ios host: 192.168.100.10

-   name: R2 device_type: cisco_ios host: 192.168.100.11

-   name: R3 device_type: cisco_ios host: 192.168.100.12

### .env (Optional)

NET_USERNAME=labuser NET_PASSWORD=labpassword NET_SECRET=labsecret

Add `.env` to `.gitignore` to protect credentials.

------------------------------------------------------------------------

## Usage

Run the script:

python autotopo.py

Output:

-   topology.png (visual network map)

------------------------------------------------------------------------

## Technologies Used

-   Python
-   Netmiko
-   PyYAML
-   NetworkX
-   Matplotlib
-   python-dotenv

------------------------------------------------------------------------

## Security & Privacy

-   No production IP addresses included
-   Credentials managed through environment variables
-   Supports mock CDP data for public GitHub deployment
-   Designed for lab and educational use

------------------------------------------------------------------------

## Future Enhancements

-   LLDP support
-   Interface labeling on topology edges
-   JSON topology export
-   Web-based interactive dashboard
-   Topology comparison engine
-   Change detection system

------------------------------------------------------------------------