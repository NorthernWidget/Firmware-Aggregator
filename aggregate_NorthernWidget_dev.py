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
all_libs_gitpath = 'https://github.com/NorthernWidget-Skunkworks/NorthernWidget-libraries.git' # Make this beforehand
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
        print(outfolder_name, "-", outmsg)
    
       
# List of all files with code

# Based on:
# https://stackoverflow.com/questions/12420779/simplest-way-to-get-the-equivalent-of-find-in-python
def listfiles(folder=os.getcwd(), extensions=None, filenames=None):
    outlist = []
    if extensions is not None:
        if type(extensions) is str:
            extensions = [extensions]
        for root, folders, files in os.walk(folder):
            for _filename in folders + files:
                if extensions == '*':
                    outlist.append(os.path.join(root, _filename))
                else:
                    for extension in extensions:
                        if extension in _filename:
                            outlist.append(os.path.join(root, _filename))
    if filenames is not None:
        if type(filenames) is str:
            filenames = [filenames]
        for root, folders, files in os.walk(folder):
            for _filename in folders + files:
                if filenames == '*':
                    outlist.append(os.path.join(root, _filename))
                else:
                    for filename in filenames:
                        if _filename == filename:
                            outlist.append(os.path.join(root, filename))
        
    return outlist

# Make sure not to double count in case root directory is shared
# between inputs and outputs
code_files = listfiles(folder=os.getcwd() + os.sep + outgit_directory, extensions=['.cpp', '.h'])
keyword_files = listfiles(folder=os.getcwd() + os.sep + outgit_directory, filenames='keywords.txt')

print ("")
print("Merging code files into single output repository")
# No check for overlapping names from different libraries
# Could do this with basenames from code_files

# If path to library folders without ".git" hidden directories is not yet given
try:
    os.mkdir(all_libs_nogit_directory_local)
except:
    pass

# This strips off the *.git but doesn't allow overwriting, hence the need to
# do this step first
#shutil.copytree( outgit_directory, all_libs_nogit_directory_local,
#                 ignore=shutil.ignore_patterns('*.git*') )


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

# Git add & commit
print("Staging files for commit")
COMMIT_MESSAGE = 'Automated update ' + str( datetime.utcnow() ) + ' UTC'
repo.index.add('*')
repo.git.add(update=True)
changedFiles = [ item.a_path for item in repo.index.diff(None) ]
if len(changedFiles) == 0:
    print("No files changed; no commit to make")
else:
    print("Committing and pushing changes")
    repo.index.commit(COMMIT_MESSAGE)
    origin = repo.remote(name='origin')
    origin.push()
print("Done")
