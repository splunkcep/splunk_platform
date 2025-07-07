# Install Multiple Splunk Apps via Bash Script

This guide explains how to automate the installation of multiple Splunk apps using `.tgz` packages on a Red Hat Linux system. The apps are extracted from a directory and installed into the Splunk apps directory.

---

## 📁 Directory Structure

- **Source directory** (with `.tgz` app files):  
  `/opt/downloads/botsv3_&_infosec_apps`

- **Destination directory** (Splunk apps):  
  `/opt/splunk/etc/apps`

---

## 🛠️ Bash Script Creation

1. Open a terminal and create the script:

   ```bash
   sudo nano /opt/downloads/install_splunk_apps.sh
   ```

2. Paste the following content:

   ```bash
   #!/bin/bash

   # Paths
   APP_SRC_DIR="/opt/downloads/botsv3_&_infosec_apps"
   SPLUNK_APPS_DIR="/opt/splunk/etc/apps"
   SPLUNK_USER="splunk"
   SPLUNK_GROUP="splunk"

   # Check if source directory exists
   if [ ! -d "$APP_SRC_DIR" ]; then
     echo "Error: Source directory '$APP_SRC_DIR' does not exist."
     exit 1
   fi

   # Create temporary directory for extraction
   TMP_DIR="/tmp/splunk_app_extract"
   mkdir -p "$TMP_DIR"

   # Loop through each .tgz file
   echo "Starting app installation from: $APP_SRC_DIR"
   for tgz_file in "$APP_SRC_DIR"/*.tgz; do
     if [ -f "$tgz_file" ]; then
       echo "Extracting $tgz_file..."
       tar -xzf "$tgz_file" -C "$TMP_DIR"

       # Get the app folder name
       app_folder=$(tar -tzf "$tgz_file" | head -1 | cut -f1 -d"/")

       if [ -d "$TMP_DIR/$app_folder" ]; then
         echo "Installing app: $app_folder"
         mv "$TMP_DIR/$app_folder" "$SPLUNK_APPS_DIR/"
         chown -R "$SPLUNK_USER:$SPLUNK_GROUP" "$SPLUNK_APPS_DIR/$app_folder"
       else
         echo "Warning: Could not identify app directory for $tgz_file"
       fi
     else
       echo "No .tgz files found in $APP_SRC_DIR"
     fi
   done

   # Cleanup
   rm -rf "$TMP_DIR"
   echo "Installation complete."

   # Prompt for Splunk restart
   read -p "Do you want to restart Splunk now? [y/N]: " RESTART_CONFIRM
   if [[ "$RESTART_CONFIRM" =~ ^[Yy]$ ]]; then
     echo "Restarting Splunk..."
     sudo /opt/splunk/bin/splunk restart
   else
     echo "Splunk restart skipped."
   fi
   ```

3. Save and exit with `CTRL+O`, `Enter`, then `CTRL+X`.

---

## 🚀 Make the Script Executable

```bash
sudo chmod +x /opt/downloads/install_splunk_apps.sh
```

---

## ▶️ Run the Script

```bash
sudo /opt/downloads/install_splunk_apps.sh
```

You’ll be prompted whether you want to restart Splunk after installing the apps.

---

## 🔍 Notes

- Ensure the `.tgz` file contains a single top-level directory representing the app.
- Apps will be installed under `/opt/splunk/etc/apps/` with correct ownership.
- Requires the Splunk service to be installed at `/opt/splunk`.

---
