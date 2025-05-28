# Preparing RHEL 9 for Splunk Enterprise Installation

This project documents the step-by-step procedure to prepare a Red Hat Enterprise Linux 9 (RHEL 9) operating system to host Splunk Enterprise.

## Table of Contents

* [Introduction](#introduction)

* [Prerequisites](#prerequisites)

* [Firewall Preparation](#firewall-preparation)

* [Next Steps](#next-steps)

## Introduction

This project documents the step-by-step procedure to prepare a Red Hat Enterprise Linux 9 (RHEL 9) operating system to host Splunk Enterprise.

## Prerequisites

Before starting, make sure :

* Red Hat Enterprise Linux 9 (RHEL 9) Operating system is already installed.
* The server has internet connectivity.
* You have Root privileges to run the commands.

## Firewall preparation

RHEL 9 typically uses `firewalld` for firewall management. We will ensure the service is installed and configure the necessary ports.

### 1. Firewall validation / installation

First, check the status of the `firewalld` service.

```bash
# Verify firewall service status
sudo systemctl status firewalld
```

If you see "active (running)", go to the section "[Open necessary ports](#open-necessary-ports)".

If you receive the message "Unit firewalld.service could not be found", then install the firewall.

```bash
# Firewall Installation (if not already installed)
sudo dnf install firewalld -y # Added -y to auto-confirm installation

# Start and enable firewall service (so it runs on boot)
sudo systemctl enable firewalld --now

# Verify firewall is running
sudo systemctl status firewalld
```

### 2. Open necessary ports

To make the most of Splunk, we need to open the following ports. We have included common Splunk ports listed in the documentation and in the preparation for other Linux distributions.

* 8000 TCP - To allow Splunk Web Interface
* 8089 TCP - To allow Splunk Management Interface / REST API
* 8443 TCP - To allow Splunk Management Interface (SSL)
* 9997 TCP - To allow communication to Universal Forwarder (Indexer Data Receiving)
* 8088 TCP - To allow communication to HTTP Event Collector (HEC)
* 8191 TCP - To allow KV Store (relevant for clustered environments)
* 443 TCP - To allow Secure Web Interface (HTTPS) if configured, or for outbound connections
* 22 TCP - To allow SSH (usually already open, but good to confirm)

```bash
# Open necessary ports permanently

# Allow Splunk Web Interface (TCP 8000)
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent

# Allow Splunk Management Interface / REST API (TCP 8089)
sudo firewall-cmd --zone=public --add-port=8089/tcp --permanent

# Allow Splunk Management Interface (SSL) (TCP 8443)
sudo firewall-cmd --zone=public --add-port=8443/tcp --permanent

# Allow Indexer Data Receiving (TCP 9997)
sudo firewall-cmd --zone=public --add-port=9997/tcp --permanent

# Allow HTTP Event Collector (HEC) (TCP 8088)
sudo firewall-cmd --zone=public --add-port=8088/tcp --permanent

# Allow KV Store (TCP 8191)
sudo firewall-cmd --zone=public --add-port=8191/tcp --permanent

# Allow Secure Web Interface (HTTPS) (TCP 443) - Optional, only needed if you configure Splunk for HTTPS on 443
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent

# Allow SSH (TCP 22) - Usually already open
sudo firewall-cmd --zone=public --add-port=22/tcp --permanent
```

### 3. Apply changes and verify

```bash
# Reload firewall to apply permanent rules to the running configuration
sudo firewall-cmd --reload

# Verify permanent configuration (list allowed ports)
sudo firewall-cmd --zone=public --list-ports --permanent
```

## Next Steps

The recommended Next Step for deploying Splunk Enterprise is [Disabling Transparent Huge Pages (THP)](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/Disable_THP_EN.md)

## References

* [Splunk Enterprise Network and Port Requirements](https://docs.splunk.com/Documentation/Splunk/9.4.1/InheritedDeployment/Ports)
