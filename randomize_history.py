import subprocess
import datetime
import random
import os

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode().strip()
    except Exception as e:
        print(f"Error running {cmd}: {e}")
        return ""

# Configuration
NEW_NAME = "Fahad Khan"
NEW_EMAIL = "fk203433@gmail.com"
DAYS_BACK = 30

# Get all commit hashes in chronological order (oldest first)
commits = run("git log --reverse --format=%H").split('\n')
commits = [c for c in commits if c]
num_commits = len(commits)

if not commits:
    print("No commits found.")
    exit(1)

print(f"Assigning random times to {num_commits} commits over the last {DAYS_BACK} days...")

# Generate sorted random timestamps
start_date = datetime.datetime.now() - datetime.timedelta(days=DAYS_BACK)
end_date = datetime.datetime.now()

# We pick N random points in the 30-day window and sort them to maintain commit order
random_timestamps = []
for _ in range(num_commits):
    # Random offset in seconds
    max_seconds = int((end_date - start_date).total_seconds())
    offset = random.randint(0, max_seconds)
    random_timestamps.append(start_date + datetime.timedelta(seconds=offset))

random_timestamps.sort()

# Start the rewrite
subprocess.run("git checkout --orphan random_history_branch", shell=True)
subprocess.run("git rm -rf .", shell=True)

for i, commit in enumerate(commits):
    ts = random_timestamps[i]
    # Add some randomness to hours/minutes if they all landed on the same second (unlikely but possible)
    # Actually they are sorted, so we just use them.
    date_str = ts.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Get message
    msg = run(f"git log -1 --format=%B {commit}")
    
    # Restore files from that commit
    subprocess.run(f"git checkout {commit} -- .", shell=True)
    subprocess.run("git add .", shell=True)
    
    # Commit with specific date and author
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = NEW_NAME
    env['GIT_AUTHOR_EMAIL'] = NEW_EMAIL
    env['GIT_COMMITTER_NAME'] = NEW_NAME
    env['GIT_COMMITTER_EMAIL'] = NEW_EMAIL
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    subprocess.run(f'git commit -m "{msg}"', shell=True, env=env)
    print(f"Successfully committed {commit[:7]} for date {date_str}")

# Replace main with random_history_branch
subprocess.run("git branch -D main", shell=True)
subprocess.run("git branch -m main", shell=True)
print("\nHistory successfully spread with organic random density.")
