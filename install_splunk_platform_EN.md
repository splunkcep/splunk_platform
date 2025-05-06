# Splunk Enterprise Setup Guide

---

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Detailed Procedure](#detailed-procedure)
- [Conclusion](#conclusion)
- [Final Notes](#final-notes)

---

## Introduction

This guide provides a detailed procedure for installing and configuring Splunk Enterprise. Aimed at technology engineers, it facilitates leveraging machine data. Learn to transform your data into operational intelligence.

## Prerequisites

Before starting, make sure you have:

* A supported operating system installed. Check [here](https://docs.splunk.com/Documentation/Splunk/9.4.1/Installation/Systemrequirements) for the list of supportes OS.
* A valid Splunk Enterprise license.
* Root permissions on OS.
* Your OS mus have proper internet connectivity.
* Python execution environment.
* All necessary ports are opened. See the [Firewall Preparation](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/FirewallPrep_EN.md) file to see step-by-step instructions to prepare your OS firewall for Splunk enterprise installation
* Transparent Hughe Pages (THP) are disables on the OS. See the [Disable THP](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/Disable_THP_EN.md) file to see  step-by-step instructions on how to disable THP.


## Installing Splunk Enterprise on Linux

### 1. Accessing the Server via SSH

Open a terminal and connect to the server via SSH:

`ssh User_Name@<Server_IP>`

* Replace:
    * User_Name by the operating system or domain user.
    * <SERVER_IP> with the actual IP of the host where you want to install Splunk.


### 2. Creating a User for Splunk

To ensure a secure installation, we will create a dedicated user to run Splunk:

```bash
# Let's create a user called splunkuser.
sudo useradd -m -r splunkuser

# Now, we have to define a password for it
sudo passwd splunkuser
```


### 3. Adding the Splunk User to the Sudo Group

Add splunkuser to the sudo group:

```bash
sudo usermod -aG sudo splunkuser

# Verify that the addition was successful:
groups splunkuser

# switch to bash
sudo chsh -s /bin/bash splunkuser

#Apply the changes by logging out and logging back in as splunkuser:
su - splunkuser
```

Where am I?
```bash
pwd
```

Who am I?
```bash
whoami
```

What do I have?
```bash
ls
```

What permissions are associated with what I have?
```bash
ls -lha
```

🔹 4️⃣ Downloading the Splunk Installer

🔹 This command:
	•	Download Splunk Enterprise version 9.4.1.
	•	If you want another version, adjust the link in wget.


```bash
sudo wget -O splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz "https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz"
```

Now, go to your downloads directory:


```bash
cd /home/splunkuser/
```

🔹 5️⃣ Adjusting Permissions on the Installation File

Before installing, check the file permissions:
```bash
ls -lha /home/splunkuser
```

Give execute permission to the file:


```bash
sudo chmod +x /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz
```

Double check the permissions:


```bash
ls -lha /home/splunkuser
```

🔹 6️⃣ Creating the Splunk Installation Directory


```bash
sudo mkdir /opt/splunk
```

Now, change the owner of the folder to the splunkuser user:


```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

```python
sudo chown -R splunkuser:splunkuser /opt/splunk
```

Check if the permissions are correct:


```python
ls -lha /opt/splunk
```

🔹 7️⃣ Installing Splunk

Extract the downloaded file to /opt
(📌 This will install Splunk in the folder /opt/splunk):


```python
tar -xzvf splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt
```

🔹 8️⃣ Starting Splunk

Now, launch Splunk and accept the license:


```python
/opt/splunk/bin/splunk start --accept-license
```

🔑
* Splunk Default Credentials:
*	OS User: splunkuser
*	OS Password: (definida anteriormente)
*	Splunk User: admin
*	Splunk Password: splunkuser

🔹 9️⃣ Setting Splunk to Start Automatically

To ensure that Splunk starts automatically when you restart the server:


```python
sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt
```

This configures the Splunk service to start automatically when the system starts.

Check the startup file:


```python
sudo vi /etc/init.d/splunk
```

Add the following lines (if necessary):


```python
RETVAL=0
USER=splunkuser
. /etc/init.d/functions
```

🔹 🔄 Basic Commands to Manage Splunk

Check status


```python
/opt/splunk/bin/splunk status
```

Launch Splunk


```python
/opt/splunk/bin/splunk start
```

Stop Splunk


```python
/opt/splunk/bin/splunk stop
```

Restart Splunk


```python
/opt/splunk/bin/splunk restart
```

Splunk is now installed and configured on your Linux server. To access it via a web browser, open:


```python
http://<IP_DO_SERVIDOR>:8000
```

