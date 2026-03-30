import json
from collections import Counter
import sys
from pathlib import Path

LOG_FILE = Path("/home/cowrie/cowrie/var/log/cowrie/cowrie.json.log")

def analyze_logs():
    if not LOG_FILE.exists():
        print(f"❌ Log file not found: {LOG_FILE}")
        print("Make sure Cowrie is running and has generated some logs.")
        return

    usernames = []
    commands = []
    downloads = 0
    sessions = 0

    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                event = json.loads(line.strip())
                
                # Count usernames
                if 'username' in event and event['username']:
                    usernames.append(event['username'])
                
                # Count commands
                if event.get('eventid') == 'cowrie.command.input':
                    cmd = event.get('input', '').strip()
                    if cmd:
                        commands.append(cmd)
                
                # Count downloads
                if event.get('eventid') == 'cowrie.download':
                    downloads += 1
                
                # Count sessions
                if event.get('eventid') == 'cowrie.session.connect':
                    sessions += 1
                    
            except (json.JSONDecodeError, KeyError):
                continue

    # Results
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

    print("\n💻 Top 10 Commands Typed:")
    for cmd, count in Counter(commands).most_common(10):
        print(f"   {count:3d} × {cmd}")

    print("\n" + "="*60)

if __name__ == "__main__":
    analyze_logs()