# Disabling Transparent Huge Pages (THP) before installing Splunk Enterprise 

Transparent Huge Pages (THP) can negatively impact Splunk performance. Therefore, Splunk recommends that this setting be disabled before installation.

## 1. Check current THP status

Before making any changes, make sure THP is enabled on your system. You can check if THP is enabled and how it's configured by looking at the enabled file in the /sys filesystem.


```bash
cat /sys/kernel/mm/transparent_hugepage/enabled
```

The output will show the current setting in square brackets [].

* `[always] madvise never`: THP is fully enabled.
* `always [madvise] never`: THP is enabled but only used for memory regions explicitly requested by applications.
* `always madvise [never]`: THP is disabled.

## 2. Edit the GRUB configuration file

The recommended way to disable THP persistently is by adding a kernel boot parameter to the GRUB configuration. 
Open the GRUB configuration file with vi (or another editor of your choice):


1.  **Edit the default GRUB configuration file:**
    ```bash
    sudo vi /etc/default/grub
    ```

2.  **Find the `GRUB_CMDLINE_LINUX` line:**
    Look for the line that starts with `GRUB_CMDLINE_LINUX="...`. This line contains the parameters passed to the kernel during boot.


3.  **Add `transparent_hugepage=never` to the line:**
    Add `transparent_hugepage=never` inside the double quotes of the `GRUB_CMDLINE_LINUX` line. Make sure to leave a space between existing parameters and the new one.

    **Example (before):**
    ```
    GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet"
    ```

    **Example (after):**
    ```
    GRUB_CMDLINE_LINUX="crashkernel=auto rhgb quiet transparent_hugepage=never"
    ```
    (The exact parameters inside the quotes may vary on your system).

4.  **Save and close the file.**

    Type [esc] then :qw then [enter]

5.  **Update the GRUB configuration:**
    You need to regenerate the GRUB configuration file that the system actually uses for booting.
    
    ```bash
    sudo grub2-mkconfig -o /boot/grub2/grub.cfg
    ```
## 4. Reboot and Verify

After modifying the GRUB configuration, you must **reboot the system** for the new kernel parameter to take effect.

```bash
sudo reboot
```

Once the server has rebooted, check the THP status again to confirm it is now set to `[never]`:

```bash
cat /sys/kernel/mm/transparent_hugepage/enabled
```

As result you should see: `always madvise [never]`

By following these steps, you will have persistently disabled Transparent Huge Pages on your Linux system.



