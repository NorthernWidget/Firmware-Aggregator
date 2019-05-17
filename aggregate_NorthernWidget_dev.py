#! /usr/bin/env/python3

"""
Clones all relevant Northern Widget repositories into a single
master repo to require only a single library install for end-users
"""

# Parser

import git
import os
import shutil

outgit_path = 'NorthernWidget__test'
combirepo_path = 'NW-libs' # Make this beforehand

# If output path is not yet made
try:
    os.mkdir(outgit_path)
except:
    pass

# Get from file list
repo_list = []
with open('repolist.txt', 'r') as f:
    repo_paths = f.read().splitlines() 

for remote_repo in repo_paths:
    outfolder_name = os.path.basename(os.path.normpath(remote_repo)).split('.')[0]
    outfolder_path = outgit_path + os.path.sep + outfolder_name
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







 
# Below here to merge into a single repository that we then upload
def recursive_overwrite(src, dest, ignore=None):
    """
    https://stackoverflow.com/questions/12683834/how-to-copy-directory-recursively-in-python-and-overwrite-all
    """
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f), 
                                    os.path.join(dest, f), 
                                    ignore)
    else:
        copyfile(src, dest)


recursive_overwrite(src=outgit_path, dest=combirepo_path, 
                    ignore=ignore_patterns('^.git'))

    
for subpath in ['src']:
    try:
        os.mkdir(outgit_path + os.path.sep + subpath)
    except:
        pass
   
