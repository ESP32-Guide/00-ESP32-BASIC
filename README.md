# 00-ESP32-BASIC

Since the script was downloaded and executed directly to stdout, it wasn't saved to a file on your system. You can re-download and run the script in one command using `wget` and `bash` together. Here's how you can do it:

1. **Download and run the installer script directly**:
    ```sh
    wget -O - https://thonny.org/installer-for-linux | bash
    ```

This command will download the installer script and pipe it directly to `bash` to execute it. Follow the prompts to complete the installation. 

If you'd rather save the script and run it manually, you can do the following:

1. **Download the script to a file**:
    ```sh
    wget -O thonny_installer.sh https://thonny.org/installer-for-linux
    ```

2. **Make the script executable**:
    ```sh
    chmod +x thonny_installer.sh
    ```

3. **Run the script**:
    ```sh
    ./thonny_installer.sh
    ```

By following these steps, you should be able to install Thonny on your system.