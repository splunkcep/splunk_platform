# Disabling Transparent Huge Pages

## What are Transparent Huge Pages?
THP is a Linux kernel feature designed to improve memory management performance by using larger memory pages (2 MB instead of the standard 4 KB). While this can benefit some applications, it can negatively impact performance for memory-intensive applications like Splunk. This is because THP's constant memory defragmentation can lead to high CPU usage and I/O latency. Disabling THP is a common and recommended practice for Splunk deployments.

## How to diable THP
You can disable THP by creating a dedicated systemd service that runs at boot time. This method is considered more reliable than editing GRUB, as it's less likely to be overwritten by kernel updates.

1. **Verify the Current THP Status**
First, check if THP is currently enabled on your system.

``` 
cat /sys/kernel/mm/transparent_hugepage/enabled
```

If the output shows [always] or [madvise], THP is active. The goal is to change this to [never].

2. **Create a Systemd Service File**
Create a new systemd service file to disable THP. Use your preferred text editor (like nano or vim).

``` 
sudo vi /etc/systemd/system/disable-thp.service
```

Paste the following content into the file: (hit 'i')

```
[Unit]
Description=Disable Transparent Huge Pages (THP)
After=network.target

[Service]
Type=oneshot
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/enabled"
ExecStart=/bin/sh -c "echo never > /sys/kernel/mm/transparent_hugepage/defrag"

[Install]
WantedBy=multi-user.target
``` 

Save and close the file. (hit [ESC], ":wq")

3. Enable and Start the New Service
Now, enable and start the service to apply the changes immediately and ensure they persist after a reboot.

```
# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to run on boot
sudo systemctl enable disable-thp.service

# Start the service immediately
sudo systemctl start disable-thp.service
```


