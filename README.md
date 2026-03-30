# SSH Honeypot with Cowrie - Threat Intelligence Lab

## Project Overview

I designed and deployed a **medium-interaction SSH/Telnet honeypot** using **Cowrie** on an Ubuntu Server virtual machine. The goal was to simulate a vulnerable Linux server, attract brute-force attacks and shell interactions, and analyze attacker behavior in a safe, isolated environment.

This project demonstrates practical skills in deception technology, log analysis, Linux administration, and basic threat hunting.

**Live Demo / Test Environment**:  
- Attacker Machine: Kali Linux  
- Honeypot Host: Ubuntu Server VM (IP: 192.168.1.8)  
- Listening Port: 2222 (can be redirected to 22 for realism)

## Objectives
- Deploy a fully functional Cowrie honeypot from source
- Simulate real-world attacks (brute-force + post-exploitation)
- Capture and analyze attacker TTPs (Tactics, Techniques, and Procedures)
- Troubleshoot common issues (virtualenv, systemd, port binding)
- Document the entire process for portfolio purposes

## Technologies & Tools Used
- **Cowrie** (Medium-interaction SSH/Telnet Honeypot)
- **Ubuntu Server** (VM)
- **Kali Linux** (attacker platform)
- Python 3 + virtualenv
- Systemd (for auto-start on boot)
- Tools: `hydra`, `ss`, `journalctl`, custom log parsing

## Architecture
Kali Linux (Attacker)
↓ (SSH on port 2222)
Ubuntu Server VM
↓
Cowrie Honeypot (Fake Linux Shell)
↓
Logs: cowrie.log + cowrie.json + tty sessions + downloaded files

## Setup Highlights

### 1. Installation
- Created dedicated low-privilege `cowrie` user
- Cloned Cowrie from GitHub
- Set up Python virtual environment
- Built fake filesystem with `createfs`
- Configured `etc/cowrie.cfg`, `userdb.txt`, and fake credentials

### 2. Configuration
- Hostname set to look like a real Ubuntu server
- SSH listening on port 2222 (0.0.0.0)
- Multiple fake users (root, admin, ubuntu, etc.)
- JSON logging enabled for easy analysis

### 3. Deployment
- Created custom systemd service that properly activates the virtual environment
- Service configured for auto-restart and boot persistence
- Tested connectivity locally and from Kali

### 4. Challenges & Solutions
- "sudo: sorry, try again" → Proper user management and no unnecessary sudo
- "Connection refused" → Fixed systemd `ExecStart` with correct virtualenv activation and port binding
- Missing scripts (`createfs`, `bin/cowrie`) → Updated to modern Cowrie commands (`cowrie start`)
- Service not listening → Refined systemd unit file

## Attack Simulation & Analysis

I simulated attacks from Kali Linux using:

- Manual SSH login with wrong passwords
- Brute-force with **Hydra** (`rockyou.txt`)
- Post-exploitation commands (`whoami`, `ls`, `cat /etc/passwd`, `wget`, `uname -a`, etc.)

**Key Findings** (replace with your actual results):
- Most common usernames attempted: root, admin, ubuntu, user
- Frequent commands: reconnaissance (`uname`, `id`, `cat /proc/cpuinfo`) and download attempts (`wget`, `curl`)
- Downloaded files stored in `var/lib/cowrie/downloads/`
- Full session replays available in `var/lib/cowrie/tty/`
