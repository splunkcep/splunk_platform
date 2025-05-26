#!/usr/bin/env python3

import os
import subprocess

def check_and_install_firewalld():
    """Check if firewalld is installed and install it if necessary."""
    print("Checking for firewalld...")
    firewalld_check = subprocess.run(["rpm", "-q", "firewalld"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    if "not installed" in firewalld_check.stdout:
        print("firewalld not found. Installing...")
        os.system("sudo yum install -y firewalld")
        os.system("sudo systemctl enable firewalld --now")
        print("firewalld successfully installed and started!")
    else:
        print("firewalld is already installed.")

def configure_firewall():
    """Configure firewalld to open port 8000."""
    print("Configuring firewall...")
    os.system("sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent")
    os.system("sudo firewall-cmd --reload")
    print("Port 8000 opened successfully!")

def create_splunk_user():
    """Create the splunkuser and set default password."""
    print("Creating splunkuser...")
    os.system("sudo useradd -m -r splunkuser")
    os.system("echo 'splunkuser:splunkuser' | sudo chpasswd")
    os.system("sudo usermod -aG wheel splunkuser")
    print("User splunkuser created and added to sudo group.")

def download_splunk():
    """Download Splunk package."""
    print("Downloading Splunk package...")
    os.system("wget -O /tmp/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz 'https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz'")
    print("Download completed!")

def prepare_installation():
    """Prepare the installation directory with correct permissions."""
    print("Preparing /opt/splunk directory...")
    os.system("sudo rm -rf /opt/splunk")
    os.system("sudo mkdir -p /opt/splunk")
    os.system("sudo chown -R splunkuser:splunkuser /opt")
    os.system("sudo chmod -R 755 /opt")
    print("/opt/splunk is ready!")

def install_splunk():
    """Extract and install Splunk."""
    print("Installing Splunk...")
    os.system("sudo -u splunkuser tar -xzvf /tmp/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt --strip-components=1")
    print("Splunk installation completed.")

def create_admin_user():
    """Create an admin user for Splunk automatically."""
    print("Creating admin user for Splunk...")
    user_seed_path = "/opt/splunk/etc/system/local/user-seed.conf"
    os.system("sudo mkdir -p /opt/splunk/etc/system/local")
    os.system("echo '[user_info]' | sudo tee {0} > /dev/null".format(user_seed_path))
    os.system("echo 'USERNAME = admin' | sudo tee -a {0} > /dev/null".format(user_seed_path))
    os.system("echo 'PASSWORD = splunkuser' | sudo tee -a {0} > /dev/null".format(user_seed_path))
    os.system("sudo chown splunkuser:splunkuser {0}".format(user_seed_path))
    os.system("sudo chmod 600 {0}".format(user_seed_path))
    print("Admin user created.")

def start_splunk():
    """Start Splunk and enable it at boot."""
    print("Starting Splunk...")
    create_admin_user()
    os.system("sudo -u splunkuser /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt")
    os.system("sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt")
    print("Splunk started and configured to auto-start on boot.")

def get_splunk_web_url():
    """Get the server IP for Splunk Web access."""
    result = subprocess.run(["hostname", "-i"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    ip_address = result.stdout.split()[0] if result.stdout else "[IP_NOT_FOUND]"
    splunk_url = f"http://{ip_address}:8000"
    print("\n\n=== SPLUNK WEB INTERFACE ===")
    print(f"Access Splunk Web by copying and pasting the link below:\n{splunk_url}\n")

def main():
    check_and_install_firewalld()
    configure_firewall()
    create_splunk_user()
    download_splunk()
    prepare_installation()
    install_splunk()
    start_splunk()
    print("Splunk Enterprise installation completed successfully!")
    get_splunk_web_url()

if __name__ == "__main__":
    main()
