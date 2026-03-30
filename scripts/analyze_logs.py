#!/usr/bin/env python3
import json
from collections import Counter
from pathlib import Path

# Try multiple possible log file locations
possible_logs = [
    Path("var/log/cowrie/cowrie.json.log"),
    Path("var/log/cowrie/cowrie.json"),
    Path("/home/cowrie/cowrie/var/log/cowrie/cowrie.json.log"),
]

log_file = None
for p in possible_logs:
    if p.exists():
        log_file = p
        break

if not log_file:
    print("❌ No Cowrie JSON log file found!")
    print("Please make some attacks first (ssh to port 2222), then try again.")
    print("Current directory:", Path.cwd())
    exit(1)

usernames = []
commands = []
downloads = 0
sessions = 0

with open(log_file, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            event = json.loads(line.strip())
            
            if 'username' in event and event.get('username'):
                usernames.append(event['username'])
            
            if event.get('eventid') == 'cowrie.command.input':
                cmd = event.get('input', '').strip()
                if cmd:
                    commands.append(cmd)
            
            if event.get('eventid') == 'cowrie.download':
                downloads += 1
            
            if event.get('eventid') == 'cowrie.session.connect':
                sessions += 1
                
        except:
            continue

print("="*60)
print("🐝 COWRIE HONEYPOT LOG ANALYSIS")
print("="*60)
print(f"Total Sessions       : {sessions}")
print(f"Total Commands       : {len(commands)}")
print(f"Files Downloaded     : {downloads}")
print(f"Unique Usernames     : {len(set(usernames))}")
print()

print("🔑 Top 10 Attempted Usernames:")
for user, count in Counter(usernames).most_common(10):
    print(f"   {count:3d} × {user}")

print("\n💻 Top 10 Commands Typed by Attackers:")
for cmd, count in Counter(commands).most_common(10):
    print(f"   {count:3d} × {cmd}")

print("\n" + "="*60)
