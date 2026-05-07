# 🛡️ Bob's Security Hub

A centralized, encrypted security suite built for Linux (Chromebook/Crostini). This project manages 2FA codes, passwords, and network security all from a single terminal interface.

## 🚀 Features

- **2FA Vault:** A TOTP generator (like Google Authenticator) that stores your secret keys behind AES encryption.
- **Password Manager:** A random password generator with an "Auto-Copy" feature (using `xclip`) and an encrypted storage vault.
- **Network Guard:** A monitoring tool to check active internet connections, scan local Wi-Fi devices (using `nmap`), and verify public/private IP addresses.
- **System Monitor:** A quick-check tool for Swap space, RAM usage, and disk health.
- **One-Click Sync:** Integrated Git commands to backup the code to GitHub while keeping sensitive data private.

## 🔒 Security Architecture

This hub uses a **Master Password** system. 
1. Your password is never stored.
2. It uses **PBKDF2** (Password-Based Key Derivation Function) with 100,000 iterations to create a secure key.
3. Data is encrypted using the **Fernet (AES-128)** standard.
4. **Permissions:** All sensitive files are locked to `chmod 600`, meaning only the owner can read or write to them.

## 🛠️ Installation & Setup

### Prerequisites
```bash
sudo apt update
sudo apt install python3-pip nmap xclip -y
pip install pyotp cryptography --break-system-packages
