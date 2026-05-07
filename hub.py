#!/usr/bin/env python3
import os
import subprocess

def clear_screen():
    os.system('clear')

def main_menu():
    while True:
        clear_screen()
        print("="*40)
        print("      BOB'S SECURITY HUB 🛡️")
        print("="*40)
        print("1. [Vault]    2FA Code Generator")
        print("2. [PassGen]  Password Manager")
        print("3. [NetGuard] Network Monitor")
        print("4. [System]   Check Stats (Swap/Disk)")
        print("5. [Lockdown] Fix File Permissions")
        print("6. [Backup]   Sync to GitHub")
        print("7. Exit")
        print("="*40)
        
        choice = input("Select an option: ")

        if choice == '1':
            subprocess.run(["python3", "/home/bob/projects/get_code.py"])
        elif choice == '2':
            subprocess.run(["python3", "/home/bob/projects/pass_gen.py"])
        elif choice == '3':
            subprocess.run(["python3", "/home/bob/projects/net_guard.py"])
        elif choice == '4':
            subprocess.run(["python3", "/home/bob/projects/tmp_check.py"])
        elif choice == '5':
            os.system("chmod 600 /home/bob/projects/*.py")
            os.system("chmod 600 /home/bob/.secrets/*.txt")
            os.system("chmod 600 ~/.git-credentials")
            input("\n✅ Permissions set to PRIVATE. Press Enter.")
        elif choice == '6':
            print("\nSyncing to GitHub...")
            os.system("cd /home/bob/projects && git add . && git commit -m 'Hub Update' && git push origin main")
            input("\n✅ Sync complete. Press Enter.")
        elif choice == '7':
            print("Shutting down Security Hub. Stay safe, Bob!")
            break
        else:
            input("Invalid choice. Press Enter.")

if __name__ == "__main__":
    main_menu()
