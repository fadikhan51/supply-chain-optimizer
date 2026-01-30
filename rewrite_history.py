import subprocess
import datetime
import os

def run(cmd):
    return subprocess.check_output(cmd, shell=True).decode().strip()

# Configuration
NEW_NAME = "Fahad Khan"
NEW_EMAIL = "fk203433@gmail.com"
DAYS_BACK = 30

# Get all commit hashes in chronological order
commits = run("git log --reverse --format=%H").split('\n')
num_commits = len(commits)

print(f"Rewriting {num_commits} commits...")

# Start date (30 days ago)
start_date = datetime.datetime.now() - datetime.timedelta(days=DAYS_BACK)

for i, commit in enumerate(commits):
    # Calculate a date that spreads commits over the 30 day period
    current_date = start_date + datetime.timedelta(days=(i * DAYS_BACK / num_commits))
    date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
    
    # Environment variables for git
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = NEW_NAME
    env['GIT_AUTHOR_EMAIL'] = NEW_EMAIL
    env['GIT_COMMITTER_NAME'] = NEW_NAME
    env['GIT_COMMITTER_EMAIL'] = NEW_EMAIL
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    # Cherry pick or rebase is complex, filter-branch is easier if squelched
    # But since we want different dates for each, we'll use a loop and git commit-tree
    
print("Setting up for history rewrite...")
# We will use a script to regenerate the branch from scratch to be safe
subprocess.run("git checkout --orphan temp_branch", shell=True)
subprocess.run("git rm -rf .", shell=True)

for i, commit in enumerate(commits):
    current_date = start_date + datetime.timedelta(days=(i * DAYS_BACK / num_commits))
    date_str = current_date.strftime('%Y-%m-%dT%H:%M:%S')
    
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

# Replace main with temp_branch
subprocess.run("git branch -D main", shell=True)
subprocess.run("git branch -m main", shell=True)
print("History rewritten successfully.")
