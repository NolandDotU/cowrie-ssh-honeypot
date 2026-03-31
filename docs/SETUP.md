# Cowrie SSH Honeypot - Detailed Setup Guide

This file contains step-bystep setup I used to deploy Cowrie honeypot.

## 1. System Prep

```bash
sudo apt update -y
sudo apt install -y git python3 python3-venv python3-dev
sudo apt install -y libssl-dev libffi-dev build-essential
```
## 2. Create Cowrie User
```bash
sudo adduser --disabled-password --gecos "" cowrie
```

## 3. Install Cowrie (as cowrie user)
```bash
sudo su - cowrie
git clone https://github.com/cowrie/cowrie.git
cd cowrie

# Create env and active it
python3 -m venv cowrie-env
source cowrie-env/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

# Config
# Copy default config
cp etc/cowrie.cfg.dist /etc/cowrie.cfg

# Edit main config
nano etc/cowrie.cfg
```

keywords for search in nano at `cowrie.cfg`:
`[honeypot]
hostname = ubuntu-prod-server-01 #whatever u want to name it
`

`[ssh]
enabled = true
listen_endpoints = tcp:2222:interface=0.0.0.0
`

`
[telnet]
enabled = true
listen_endpoints = tcp:2323:interface=0.0.0.0
`

`
[output_jsonlog]
enabled = true
`

## 5. Create Fake Credentials
```bash
nano etc/userdb.txt
```
add
`
root:0:*
admin:1000:password123
ubuntu:1000:ubuntu
user:1000:password
`

## 6 Build Fake Filesystem
```bash
mkdir -p share/cowrie
createfs -l honeyfs -o share/cowrie/fs.pickle -v
```

## 7. Systemd service setup (for auto start it on Boot)
```bash
sudo cat > /etc/systemd/system/cowrie.service << 'EOF'
[Unit]
Description=Cowrie SSH/Telnet Honeypot
After=network.target

[Service]
Type=simple
User=cowrie
Group=cowrie
WorkingDirectory=/home/cowrie/cowrie
ExecStart=/bin/bash -c 'cd /home/cowrie/cowrie && source cowrie-env/bin/activate && exec cowrie start'
ExecStop=/bin/bash -c 'cd /home/cowrie/cowrie && source cowrie-env/bin/activate && exec cowrie stop'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```
enable it and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable cowrie
sudo systemctl start cowrie
sudo systemctl status cowrie
```

8.Verify Installation (just in case)
```bash
# Check if port 2222 is listening
sudo ss -tlnp | grep 2222

# View live logs
sudo journalctl -u cowrie -f
```
## 9. Test it using your different device
```bash
ssh -p 2222 root@<YOUR-COWRIE-IP>
```

