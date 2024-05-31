import os
import platform
import psutil
import subprocess
import time

# List of known screenshot process names
screenshot_processes = ['screencap', 'screenshot', 'snippingtool', 'Snip & Sketch', 'Grab', 'gnome-screenshot']

def kill_process(pid, name):
    try:
        print(f"Terminating process: {name} (PID: {pid})")
        if platform.system() == 'Windows':
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            os.kill(pid, 9)
    except Exception as e:
        print(f"Failed to terminate process {name} (PID: {pid}): {e}")

def kill_screenshot_processes():
    while True:
        # Iterate through all running processes using psutil
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Check if the process name matches any known screenshot process
                if proc.info['name'] in screenshot_processes:
                    kill_process(proc.info['pid'], proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Additional handling for Termux (Android)
        if platform.system() == 'Linux' and 'ANDROID_ROOT' in os.environ:
            result = subprocess.run(['ps', '-A'], stdout=subprocess.PIPE)
            processes = result.stdout.decode('utf-8').splitlines()

            for process in processes:
                for proc_name in screenshot_processes:
                    if proc_name in process:
                        pid = int(process.split(None, 1)[0])
                        kill_process(pid, proc_name)

        # Sleep for a short interval before checking again
        time.sleep(1)

if __name__ == '__main__':
    print("Starting screenshot protection service...")
    try:
        kill_screenshot_processes()
    except KeyboardInterrupt:
        print("Stopping screenshot protection service...")
