#! /usr/bin/env python3

"""
Clones all relevant Northern Widget repositories into a single
master repo to require only a single library install for end users.

(Install via copy/paste)

Written by A. Wickert
"""

import git
import os
import shutil
import glob
from datetime import datetime

outgit_directory = 'NWraw'
all_libs_directory_git = 'NorthernWidget-libraries'
all_libs_gitpath = 'https://github.com/NorthernWidget/NorthernWidget-libraries.git' # Make this beforehand
git_remoteurl = 'git@github.com:NorthernWidget-Skunkworks/NorthernWidget-libraries.git'

# If output path is not yet made
try:
    os.mkdir(outgit_directory)
except:
    pass

# Get from file list
repo_list = []
with open('repolist.txt', 'r') as f:
    repo_paths = f.read().splitlines() 
    
# Remove comments and blank lines
_topop = []
for i in range(len(repo_paths)):
    if len(repo_paths[i]) == 0:
        _topop.append(i)
    elif repo_paths[i][0] == '#':
        _topop.append(i)

# Pop the blank lines from the list -- need to start at the highest
# indices so the index positions are not shifted.
# We indexed from lowest to highest in the loop, so just need to reverse order
_topop = _topop[::-1]

for i in _topop:
    repo_paths.pop(i)

for remote_repo in repo_paths:
    outfolder_name = os.path.basename(os.path.normpath(remote_repo)).split('.')[0]
    outfolder_path = outgit_directory + os.path.sep + outfolder_name
    try:
        # If not yet cloned
        git.Repo.clone_from(remote_repo, outfolder_path)
        print(outfolder_name, "successfully cloned.")
    except:
        # Otherwise, pull an update
        g = git.cmd.Git(outfolder_path)
        outmsg = g.pull()
        print("Pulling updates from", outfolder_name, "-", outmsg)
       
print ("")
print("Merging code files into single output repository")
# No check for overlapping names from different libraries
# Could do this with basenames from code_files

# If path to library folders without ".git" hidden directories is not yet given
try:
    os.mkdir(all_libs_nogit_directory_local)
except:
    pass

# Then clone/update the git repo
try:
    # If repo doesn't exist, check it out
    repo = git.Repo.clone_from(git_remoteurl, all_libs_directory_git)
    print(all_libs_directory_git, "successfully cloned.")
except:
    repo = git.Repo(all_libs_directory_git)
    outmsg = repo_origin = repo.remotes.origin
    repo_origin.pull()
    print("Updates pulled from", all_libs_directory_git, "-", outmsg)

# glob ignores hidden files by default (including those from git)
paths_at_origin = glob.glob(outgit_directory+'/**', recursive=True)
filenames_at_origin = [f for f in paths_at_origin if os.path.isfile(f)]
paths_at_git_directory = []
for filename in filenames_at_origin:
    paths_at_git_directory.append( all_libs_directory_git
                                   + filename.split(outgit_directory)[-1] )

# And then copy them into the destination folder
for i in range(len(paths_at_git_directory)):
    source = filenames_at_origin[i]
    dest = paths_at_git_directory[i]
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy(source, dest)
print("Updates added to", all_libs_directory_git)

# Git add & commit

print("Staging files for commit")
COMMIT_MESSAGE = 'Automated update ' + str( datetime.utcnow() ) + ' UTC'
repo.index.add('*')
repo.git.add(update=True)
stagedChanges = repo.index.diff("HEAD")
if len(stagedChanges) == 0:
    print("No files changed; no commit to make")
else:
    print("Committing and pushing changes")
    repo.index.commit(COMMIT_MESSAGE)
    print("Commit message:", COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
print("Done")
