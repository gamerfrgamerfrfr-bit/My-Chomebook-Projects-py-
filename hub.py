#!/usr/bin/env python3
import os
import subprocess

def clear_screen():
    os.system('clear')

def main_menu():
    while True:
        clear_screen()
        print("="*35)
        print("      BOB'S SECURITY HUB 🛡️")
        print("="*35)
        print("1. [Vault]    Get 2FA Codes")
        print("2. [System]   Check Stats (Swap/Disk)")
        print("3. [Lockdown] Fix File Permissions")
        print("4. [Backup]   Sync to GitHub")
        print("5. [NetGuard] Monitor Network")
        print("6. Exit")
        print("="*35)
        
        choice = input("Select an option: ")

        if choice == '1':
            subprocess.run(["python3", "/home/bob/projects/get_code.py"])
        elif choice == '2':
            subprocess.run(["python3", "/home/bob/projects/tmp_check.py"])
        elif choice == '3':
            # Secure all project files
            os.system("chmod 600 /home/bob/projects/*.py")
            os.system("chmod 600 /home/bob/.secrets/vault.txt")
            os.system("chmod 600 ~/.git-credentials")
            input("\n✅ Permissions set to PRIVATE. Press Enter.")
        elif choice == '4':
            print("\nSyncing to GitHub...")
            os.system("cd /home/bob/projects && git add . && git commit -m 'Hub Update' && git push origin main")
            input("\n✅ Sync complete. Press Enter.")
        elif choice == '5':
            subprocess.run(["python3", "/home/bob/projects/net_guard.py"])
        elif choice == '6':
            print("Shutting down Security Hub. Stay safe, Bob!")
            break
        else:
            input("Invalid choice. Press Enter to try again.")

if __name__ == "__main__":
    main_menu()
