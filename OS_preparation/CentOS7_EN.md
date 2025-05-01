# Preparing CentOS7 for Splunk Enterprise Installation

This project documents the step-by-step procedure to prepare a CentOS7 operating system to host Splunk Enterprise

## Table of Contents

* [Introduction](#introduction)

* [Prerequisites](#prerequisites)

* [Firewall Preparation](#firewall-preparation)

* [Next Steps](#next-steps)

---

## Introduction

This project documents the step-by-step procedure to prepare a CentOS7 operating system to host Splunk Enterprise

## Prerequisites

Before starting, make sure :

* Already installed CentOS7 Operating system

* The server has internet connectivity

* You have Root privileges to run the commands

## Firewall preparation

CentOS 7 typically uses `iptables` for firewall management. We will ensure the `iptables-services` package is installed and configure the necessary ports.

### 1. Firewall validation / installation

First, check the status of the `iptables` service.

```bash
# Verify iptables service status
sudo systemctl status iptables
```

If you see "active (exited)" or "active (running)", the service is likely installed. If you get a message indicating the service is not found or is inactive, you may need to install and enable the `iptables-services` package.

```bash
# Install iptables-services (if not installed)
sudo yum install -y iptables-services

# Enable iptables service to start on boot
sudo systemctl enable iptables

# Start iptables service now
sudo systemctl start iptables

# Verify iptables service is running
sudo systemctl status iptables
```

### 2. Open necessary ports

We will add `iptables` rules to open the necessary ports for Splunk. These rules will be inserted at the beginning of the `INPUT` chain.

Based on the common Splunk ports (as seen in the "Common Splunk Enterprise Default Ports" document):

* 8000 TCP - To allow Splunk Web Interface

* 8089 TCP - To allow Splunk Management Interface / REST API
  
* 8443 TCP - To allow Splunk Management Interface (SSL)

* 9997 TCP - To allow communication to Universal Forwarder

* 8088 TCP - To allow communication to HTTP Event Collector (HEC)

* 8191 TCP - To allow KV Store (relevant for clustered environments)

* 443 TCP - To allow Secure Web Interface (HTTPS) if configured, or for outbound connections

* 22 TCP - To allow SSH (usually already open, but good to confirm)

```bash
# Open necessary ports using iptables

# Allow Splunk Web Interface (TCP 8000)
sudo iptables -I INPUT -p tcp --dport 8000 -j ACCEPT

# Allow Splunk Management Interface / REST API (TCP 8089)
sudo iptables -I INPUT -p tcp --dport 8089 -j ACCEPT

# Allow Indexer Data Receiving (TCP 9997)
sudo iptables -I INPUT -p tcp --dport 9997 -j ACCEPT

# Allow HTTP Event Collector (HEC) (TCP 8088)
sudo iptables -I INPUT -p tcp --dport 8088 -j ACCEPT

# Allow KV Store (TCP 8191)
sudo iptables -I INPUT -p tcp --dport 8191 -j ACCEPT

# Allow Secure Web Interface (HTTPS) (TCP 443)
sudo iptables -I INPUT -p tcp --dport 443 -j ACCEPT

# Allow SSH (TCP 22) - Usually already open
sudo iptables -I INPUT -p tcp --dport 22 -j ACCEPT
```

### 3. Save rules for persistence and verify

To ensure these `iptables` rules persist after a reboot, you need to save the current rules. The `iptables-services` package handles loading these saved rules automatically on boot if the service is enabled.

```bash
# Save current iptables rules to the default file
sudo service iptables save

# Verify the rules were saved (optional)
# cat /etc/sysconfig/iptables

# Verify the rules are currently active
sudo iptables -nvL
```

## Next Steps

The recommended Next Step for deploying Splunk Enterprise is [Disabling Transparent Huge Pages (THP)](XXXXX)
