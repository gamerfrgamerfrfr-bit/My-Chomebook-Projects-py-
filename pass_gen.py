#!/usr/bin/env python3
import os
import random
import string
import base64
import subprocess
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

PASS_VAULT = "/home/bob/.secrets/passwords.txt"
SALT = b'bob_chromebook_secure_123'

def get_crypto_key(password):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000)
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

def load_all_passwords(cipher):
    if not os.path.exists(PASS_VAULT) or os.stat(PASS_VAULT).st_size == 0:
        return []
    with open(PASS_VAULT, "rb") as f:
        try:
            decrypted = cipher.decrypt(f.read()).decode()
            return [line for line in decrypted.splitlines() if ":" in line]
        except:
            print("❌ Access Denied: Incorrect Password.")
            exit()

def save_all_passwords(cipher, lines):
    data = "\n".join(lines).encode()
    encrypted = cipher.encrypt(data)
    with open(PASS_VAULT, "wb") as f:
        f.write(encrypted)

def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def copy_to_clipboard(text):
    try:
        process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
        process.communicate(input=text.encode())
        return True
    except FileNotFoundError:
        return False

def main():
    os.system('clear')
    print("="*45)
    print("      🔐 BOB'S STEALTH PASSWORD VAULT")
    print("="*45)
    
    master_pw = input("🔑 Enter Master Password: ")
    cipher = get_crypto_key(master_pw)
    lines = load_all_passwords(cipher)

    while True:
        print("\n" + "-"*45)
        print("1. [Generate] Create & Copy new password")
        print("2. [Select]   Pick account to Copy to clipboard")
        print("3. [Delete]   Remove a password")
        print("4. [Exit]     Back to Hub")
        print("-"*45)
        
        choice = input("Select an option: ")

        if choice == '1':
            new_pass = generate_password()
            # We show it once during generation so you can see what it is
            print(f"\n✨ New Password: {new_pass}")
            copy_to_clipboard(new_pass)
            print("📋 Copied to clipboard!")
            
            confirm = input("Save this? (y/n): ").lower()
            if confirm == 'y':
                label = input("Label (e.g., Discord): ").strip()
                lines.append(f"{label}:{new_pass}")
                save_all_passwords(cipher, lines)
                print(f"✅ Saved!")
        
        elif choice == '2':
            print("\n--- SAVED ACCOUNTS ---")
            if not lines:
                print("Vault is empty.")
            else:
                for i, line in enumerate(lines):
                    label, _ = line.split(":")
                    print(f"{i+1}. {label}")
                
                pick = input("\nEnter number to copy password (or 'b' for back): ")
                if pick.isdigit() and 1 <= int(pick) <= len(lines):
                    selected_line = lines[int(pick)-1]
                    label, pw = selected_line.split(":")
                    copy_to_clipboard(pw)
                    print(f"✅ Password for {label} copied to clipboard! (Ready to Paste)")
                else:
                    print("Returning...")

        elif choice == '3':
            target = input("Enter the label to delete: ").strip()
            new_lines = [l for l in lines if not l.startswith(f"{target}:")]
            if len(new_lines) < len(lines):
                save_all_passwords(cipher, new_lines)
                lines = new_lines
                print(f"🗑️ Deleted {target}.")
            else:
                print("❌ Label not found.")

        elif choice == '4':
            break

if __name__ == "__main__":
    main()
