#! /usr/bin/env/python3

"""
Clones all relevant Northern Widget repositories into a single
master repo to require only a single library install for end-users
"""

# Parser

import git
import os
from shutil import copyfile

outgit_path = 'NorthernWidget__test'

# Get from file list
repo_list = []
with open('../repolist.txt', 'r') as f:
    repo_paths = f.read().splitlines() 

for remote_repo in repo_paths:
    outfolder_name = os.path.basename(os.path.normpath(remote_repo)).split('.')[0]
    try:
        # If not yet cloned
        git.Repo.clone_from(remote_repo, outfolder_name)
        print(outfolder_name, "successfully cloned.")
    except:
        # Otherwise, pull an update
        g = git.cmd.Git(outfolder_name)
        outmsg = g.pull()
        print(outfolder_name, "-", outmsg)
    
        
# If output path is not yet made
try:
    os.mkdir(outgit_path)
except:
    pass
for subpath in ['src']:
    try:
        os.mkdir(outgit_path + os.path.sep + subpath)
    except:
        pass

# List of all files with code

# Based on:
# https://stackoverflow.com/questions/12420779/simplest-way-to-get-the-equivalent-of-find-in-python
def listfiles(folder=os.getcwd(), extensions=None):
    outlist = []
    if type(extensions) is str:
        extensions = [extensions]
    for root, folders, files in os.walk(folder):
        for filename in folders + files:
            if extensions is None:
                outlist.append(os.path.join(root, filename))
            else:
                for extension in extensions:
                    if extension in filename:
                        outlist.append(os.path.join(root, filename))
    return outlist

# Make sure not to double count in case root directory is shared
# between inputs and outputs
codefiles = []
codefiles_raw = listfiles(extensions=['.cpp', '.h'])
for codefile in codefiles_raw:
    if outgit_path not in codefile:
        codefiles.append(codefile)

print ("")
print("Merging code files into single output repository")
print(" >>> Warn: add check to see if file already exists")
for codefile in codefiles:
    copyfile(codefile, outgit_path + os.sep + 'src' + os.sep +  os.path.basename(os.path.normpath(codefile)))
    
