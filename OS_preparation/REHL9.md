# Splunk Enterprise Setup Guide

## Table of Contents

* [Introduction](#introduction)

* [Prerequisites](#prerequisites)

* [Detailed Procedure](#detailed-procedure)

* [Conclusion](#conclusion)

* [Final Notes](#final-notes)

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

* Transparent Huge Pages (THP) are disabled on the OS. See the [Disable THP](https://github.com/splunkcep/splunk_platform/blob/main/OS_preparation/Disable_THP_EN.md) file to see step-by-step instructions on how to disable THP.

## Installing Splunk Enterprise on Linux

### 1. Accessing the Server via SSH

Open a terminal and connect to the server via SSH:

`ssh User_Name@<Server_IP>`

* Replace:

  * User_Name by the operating system or domain user.

  * `<SERVER_IP>` with the actual IP of the host where you want to install Splunk.

### 2. Creating a User for Splunk

To ensure a secure installation, we will create a dedicated user to run Splunk:

```
# Let's create a user called splunkuser.
sudo useradd -m -r splunkuser

# Now, we have to define a password for it
sudo passwd splunkuser


```

### 3. Adding the Splunk User to the Sudo/Wheel Group

1. Add `splunkuser` to the appropriate group for `sudo` privileges:

   **CentOS / RHEL**

   ```
   sudo usermod -aG wheel splunkuser
   
   
   ```

   **Ubuntu**

   ```
   sudo usermod -aG sudo splunkuser
   
   
   ```

2. Verify that the addition was successful:

   ```
   groups splunkuser
   
   
   ```

3. Switch to bash (if necessary):

   **CentOS / RHEL / Ubuntu**

   ```
   # Validate your SHELL, which should ideally be /bin/bash
   su - splunkuser
   echo $SHELL
   
   
   ```

   *(Note: The `su - splunkuser` command will log you in as `splunkuser` with their default shell. If `chsh` is needed to change the default shell, it should be done before `su -`)*

   Apply the changes by logging out and logging back in as `splunkuser`:

   ```
   exit # Exit current session if you used 'su - splunkuser'
   ssh splunkuser@<Server_IP> # Log back in as splunkuser
   
   
   ```

   Alternatively, if you are already logged in as `splunkuser` after `su - splunkuser`, you can simply `exit` and then `su - splunkuser` again to ensure group changes are applied.

### 4. Downloading the Splunk Installer

Go to <https://www.splunk.com/en_us/download/splunk-enterprise.html> and

* Log in if requested (requires Splunk.com user)

* Select *Linux* as Operating System

* at the *.tgz* option, click on *Copy wget link* and copy the `wget` command shown

Execute the command with `sudo`. This downloads Splunk Enterprise version 9.X.X.

```
# This is an EXAMPLE. Use the wget command copied from the download page.
cd /home/splunkuser/
sudo wget -O splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz "[https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz](https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz)"


```

Now, go to the directory you downloaded the file and validate the file is found:

```
cd /home/splunkuser/
ls


```

### 5. Adjusting Permissions on the Installation File

Before installing, check the file permissions:

```
ls -lha /home/splunkuser


```

You will notice `splunkuser` currently has read permissions on the file but cannot execute, modify or delete it without `sudo` or a change in ownership or granting the proper permissions.
Give execute permission to the file:

```
sudo chmod +x /home/splunkuser/splunk-9.4.2-e9664af3d956-linux-amd64.tgz


```

Double check the permissions:

```
ls -lha /home/splunkuser


```

The permissions are now `-rwxr-xr-x`. This means `splunkuser` can read the file (r) and can now execute it (x).

### 6. Creating the Splunk Installation Directory

The following command will create the splunk directory:

```
sudo mkdir /opt/splunk


```

This creates the folder, but only `root` has permissions over it. You can check it running:

```
ls -lha /opt/splunk


```

Then, let's change the owner of the folder to the `splunkuser` user and validate the permissions:

```
#Changes the ownership of the folder
sudo chown -R splunkuser:splunkuser /opt/splunk

#checks the permissions on the folder
ls -lha /opt/splunk


```

### 7. Installing Splunk

Extract the downloaded file to `/opt`. This will install Splunk in the folder `/opt/splunk`:

```
tar -xzvf splunk-9.4.2-e9664af3d956-linux-amd64.tgz -C /opt


```

### 8. Starting Splunk

Now, launch Splunk and accept the license:

```
/opt/splunk/bin/splunk start --accept-license


```

This will prompt you to define an Administrator username and password. Set it appropriately.

🔑

* Splunk Default Credentials:

* OS User: `splunkuser`

* OS Password: (previously defined)

* Splunk User: `admin`

* Splunk Password: `splunkuser` (or any other you define)

### 9. Setting Splunk to Start Automatically

To ensure Splunk starts automatically when you restart the server, we'll use Splunk's built-in boot-start functionality, which integrates with **systemd**, the default service manager on CentOS 7 and 8, RHEL 7 and 8, and modern Ubuntu versions.

Execute the following command. The `-systemd-managed 1` flag explicitly tells Splunk to configure itself as a systemd service.

```
sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt -systemd-managed 1


```

This command creates and enables a `systemd` service unit for Splunk, allowing it to start automatically on system boot.

### 10. Verify Splunk's Systemd Service

After running the command, you can verify the service status and ensure it's enabled to start on boot:

1. **Check the service status:**

   ```
   systemctl status Splunkd.service
   
   
   ```

   You should see output indicating that the service is `active (running)`.

2. **Verify if it's enabled to start on boot:**

   ```
   systemctl is-enabled Splunkd.service
   
   
   ```

   This command should output `enabled`. If for any reason it's not enabled, you can enable it manually (though the `enable boot-start` command should handle this):

   ```
   sudo systemctl enable Splunkd.service
   
   
   ```

## Basic Commands to Manage Splunk

Check status

```
/opt/splunk/bin/splunk status


```

Launch Splunk

```
/opt/splunk/bin/splunk start


```

Stop Splunk

```
/opt/splunk/bin/splunk stop


```

Restart Splunk

```
/opt/splunk/bin/splunk restart


```

Splunk is now installed and configured on your Linux server. To access it via a web browser, open:

```
http://<SERVER_IP>:8000


