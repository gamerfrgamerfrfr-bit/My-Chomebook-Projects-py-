#!/usr/bin/env python3
import os
import random
import string
import base64
import time
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
    # Mix of Uppercase, Lowercase, Numbers, and Symbols
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(chars) for _ in range(length))

def main():
    os.system('clear')
    print("="*45)
    print("      🔐 BOB'S PASSWORD VAULT")
    print("="*45)
    
    master_pw = input("🔑 Enter Master Password: ")
    cipher = get_crypto_key(master_pw)
    lines = load_all_passwords(cipher)

    while True:
        print("\n" + "-"*45)
        print("1. [Generate] Create a new password")
        print("2. [View]     See all saved passwords")
        print("3. [Delete]   Remove a password")
        print("4. [Exit]     Back to Hub")
        print("-"*45)
        
        choice = input("Select an option: ")

        if choice == '1':
            new_pass = generate_password()
            print(f"\n✨ Suggested Password: {new_pass}")
            confirm = input("Save this? (y/n): ").lower()
            if confirm == 'y':
                label = input("Label (e.g., Discord, School): ").strip()
                lines.append(f"{label}:{new_pass}")
                save_all_passwords(cipher, lines)
                print(f"✅ Saved password for {label}!")
        
        elif choice == '2':
            print("\n--- YOUR SAVED PASSWORDS ---")
            if not lines:
                print("Vault is empty.")
            for line in lines:
                label, pw = line.split(":")
                print(f"{label:<15} | {pw}")
            input("\nPress Enter to hide passwords...")
            os.system('clear')

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
