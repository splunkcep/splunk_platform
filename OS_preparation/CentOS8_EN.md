# Preparing CentOS8 for Splunk Enterprise Installation

This project documents the step-by-step procedure to prepare a CentOS8 operating system to host Splunk Enterprise
---

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Firewall Preparation](#detailed-procedure)
- [Next Steps](#conclusion)

---

## Introduction

This project documents the step-by-step procedure to prepare a CentOS8 operating system to host Splunk Enterprise

## Prerequisites

Before starting, make sure :

- Already installed CentOs8 Operating system
- The server has internet connectivity
- You have Root privileges to run the commands

# Firewall preparation

## 1. Firewall validation / installation

```bash
# Verify firewall is running
sudo systemctl status firewalld
```
If you see "active (running)" go to "[Open Ports Section](#2-open-necessary-ports)"

If you get the message "Unit firewalld.service could not be found" the firewall then install it.

```bash
# Firewall Installation (if not already installed)
sudo dnf install firewalld -y # Added -y to auto-confirm installation

# Start and enable firewall service (so it runs on boot)
sudo systemctl enable firewalld —now

# Verify firewall is running
sudo systemctl status firewalld
```

## 2. Open necessary ports

In order to make the most of Splunk, we need to open the following ports:
- 8000 TCP - To allow Splunk Web Interface
- 8443 TCP - To allow Splunk Management Interface (SSH)
- 443 TCP - To allow Secure Web Interface (HTTPS)
- 8088 TCP - To allow communication to HTTP Event Colector (HEC)
- 9997 TCP - To allow communication to Universal Forwarder

```bash
# Open necessary ports permanently

# Allow Splunk Web Interface
sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent

# Allow Splunk Management Interface (SSL)
sudo firewall-cmd --zone=public --add-port=8443/tcp --permanent

# Allow Secure Web Interface (HTTPS) - Optional, only needed if you configure Splunk for HTTPS on 443
sudo firewall-cmd --zone=public --add-port=443/tcp --permanent

# Allow HTTP Event Collector (HEC)
sudo firewall-cmd --zone=public --add-port=8088/tcp --permanent

# Allow Universal Forwarder Port
sudo firewall-cmd --zone=public --add-port=9997/tcp --permanent
```

##3. Apply changes and verify

```bash
# Reload firewall to apply permanent rules to the running configuration
sudo firewall-cmd --reload

# Verify permanent configuration
sudo firewall-cmd --zone=public --list-ports --permanent
```

# Next Steps

The recommended Next Step for deploying Splunk Enterprise is [Disabling Transparent Huge Pages (THP)](XXXXX)

