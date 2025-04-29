# Splunk Enterprise Automated Installation for Linux

This project provides fully automated Python scripts to install and configure **Splunk Enterprise 9.4.1** on multiple Linux distributions, including:

- CentOS 7 (Core)
- CentOS 8
- Ubuntu 20.04 / 22.04
- Debian 10 / 11

The goal is to simplify and accelerate the deployment of Splunk Enterprise, following professional best practices, ensuring that the installation is stable, secure, and ready for further use with applications like Enterprise Security (ES) or ITSI.

---

## Table of Contents

- [About This Project](#about-this-project)
- [Supported Linux Versions](#supported-linux-versions)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Splunk Default Access](#splunk-default-access)
- [Author](#author)
- [License](#license)

---

## About This Project

Each script in this repository performs the following tasks automatically:
- Verifies and installs necessary system packages (such as `firewalld` or `ufw`).
- Configures the firewall to allow Splunk Web traffic (port 8000/TCP).
- Creates a dedicated system user (`splunkuser`) for Splunk.
- Downloads the latest Splunk Enterprise package.
- Prepares the installation directory with correct permissions (`/opt/splunk`).
- Extracts and installs Splunk.
- Creates an initial admin user with default credentials.
- Starts Splunk and configures it to autostart on system boot.
- Displays the Splunk Web URL based on the server's IP address.

---

## Supported Linux Versions

| Distribution  | Versions Supported |
|:--------------|:-------------------|
| CentOS        | 7, 8 |
| Ubuntu        | 20.04 LTS, 22.04 LTS |
| Debian        | 10 (Buster), 11 (Bullseye) |

> **Note:**  
> Future support for RHEL, AlmaLinux, Rocky Linux and others may be added.

---

## Prerequisites

Before running the script, ensure that you have:

- A clean Linux server (CentOS, Ubuntu, or Debian).
- Internet access from the server (to download Splunk and install packages).
- `sudo` privileges on the machine.
- Python 3 installed (install with `sudo yum install -y python3` or `sudo apt install -y python3` if needed).

---

## Installation Steps

1. Clone or download this repository:
   ```bash
   git clone https://github.com/your-repo/splunk-linux-install.git
   cd splunk-linux-install
