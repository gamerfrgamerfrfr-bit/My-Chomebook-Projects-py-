#!/usr/bin/env python3
import os
import subprocess

def run_command(cmd):
    try:
        # Runs the shell command and captures the output
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode()
    except subprocess.CalledProcessError:
        return "No data found or command failed."

def main():
    while True:
        os.system('clear')
        print("="*45)
        print("       🛰️  BOB'S NETWORK GUARD")
        print("="*45)
        print("1. [Connections] What is my PC talking to?")
        print("2. [Radar] Scan for other devices on Wi-Fi")
        print("3. [Ports] Check for open 'doors' on my PC")
        print("4. [IP] Show my local and public IP")
        print("5. Return to Hub")
        print("="*45)
        
        choice = input("Select an option: ")

        if choice == '1':
            print("\n--- ACTIVE INTERNET CONNECTIONS ---")
            # Lists active TCP connections (ESTABLISHED)
            print(run_command("ss -tunp | grep ESTAB || echo 'No active connections.'"))
            input("\nPress Enter to continue...")

        elif choice == '2':
            print("\n--- SCANNING LOCAL NETWORK ---")
            print("Note: On Chromebooks, this shows the virtual bridge.")
            # This scans the standard local network range
            print(run_command("nmap -sn 192.168.1.0/24 | grep 'Nmap scan report'"))
            input("\nPress Enter to continue...")

        elif choice == '3':
            print("\n--- OPEN PORTS (LISTENING) ---")
            # Shows which services are waiting for a connection
            print(run_command("ss -tulpn | grep LISTEN"))
            input("\nPress Enter to continue...")
            
        elif choice == '4':
            print("\n--- IP ADDRESS INFO ---")
            print("Local IP:", run_command("hostname -I").strip())
            print("Public IP:", run_command("curl -s ifconfig.me"))
            input("\nPress Enter to continue...")

        elif choice == '5':
            break

if __name__ == "__main__":
    main()
