import os
import platform
import subprocess
import time

def take_screenshot():
    # Define the screenshot file name with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_file = f"screenshot_{timestamp}.png"

    if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
        # For Termux (Android)
        screenshot_path = f"/sdcard/{screenshot_file}"
        command = f"screencap -p {screenshot_path}"
    elif platform.system() == 'Windows':
        # For Windows
        screenshot_path = screenshot_file
        command = f"powershell -command \"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{{PRTSC}}'); Start-Sleep -Milliseconds 500; [System.Drawing.Bitmap]::FromHbitmap([System.Windows.Forms.Clipboard]::GetImage().GetHbitmap()).Save('{screenshot_path}');\""
    elif platform.system() == 'Darwin':
        # For macOS
        screenshot_path = f"~/Desktop/{screenshot_file}"
        command = f"screencapture -x {screenshot_path}"
    else:
        # For Linux
        screenshot_path = f"~/Pictures/{screenshot_file}"
        command = f"import -window root {screenshot_path}"

    # Execute the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Check for errors
    if process.returncode != 0:
        print(f"Error taking screenshot: {stderr.decode('utf-8')}")
        return None

    print(f"Screenshot saved to {screenshot_path}")
    return screenshot_path

if __name__ == "__main__":
    print("Starting screenshot service...")
    if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
        # Request storage permissions if not already granted (Termux specific)
        print("Requesting storage permissions...")
        os.system("termux-setup-storage")

    # Take a screenshot
    take_screenshot()
