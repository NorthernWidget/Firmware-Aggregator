#! /usr/bin/env/python3

"""
Clones all relevant Northern Widget repositories into a single
master repo to require only a single library install for end-users
"""

# Parser

import git
import os
import shutil

outgit_directory = 'NWraw'
combirepo_directory = 'NW-libs' # Make this beforehand

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
                if extensions is '*':
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
                if filenames is '*':
                    outlist.append(os.path.join(root, _filename))
                else:
                    for filename in filenames:
                        if _filename == filename:
                            outlist.append(os.path.join(root, filename))
        
    return outlist

# Make sure not to double count in case root directory is shared
# between inputs and outputs
code_files = listfiles(extensions=['.cpp', '.h'])
keyword_files = listfiles(filenames='keywords.txt')

print ("")
print("Merging code files into single output repository")
# No check for overlapping names from different libraries
# Could do this with basenames from code_files

# Also: no check that these files are in the current desired output directory


# If output path is not yet made
try:
    os.mkdir(combirepo_path)
except:
    pass

for code_file in code_files:
    outpath = combirepo_directory + os.sep +  os.path.basename(os.path.normpath(code_file))
    shutil.copyfile(code_file, outpath)

# Eventually: add tool to combine keywords.txt with appropriate preservation
# of the different sections for syntax highlighting


