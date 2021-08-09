#! /usr/bin/env python3

import re
import argparse
import os
import shutil

#a script to pull out alignment info files from a collection of them based on a provided list file
#this script is based on get_interesting_alignments.py, but is using different files and therefore has different formatting

def pull_info_files():
    try:
        with open("{0}".format(args.listfile), "r") as list_file:
            print("opened list file")
            try:
                os.mkdir("{0}".format(args.newdir))
            except FileExistsError:
                print("This directory already exists. Please provide a different name")
            #put all the mouse names in the file into a set for checking against
            mouse_names = set()
            for name in list_file:
                mouse_names.add(name.strip())
            #go through all the files in the directory, find the ones that match the names in the set
            for item in os.scandir("{0}".format(args.aligndir)):
                just_name = re.match("(Mus_musculus\|\d+_rename)\.phylip\.iqtree", "{0}".format(item.name))
                if just_name.group(1) in mouse_names:
                    #copy the ones that match into the directory you made earlier
                    destination = os.path.join(args.newdir, item.name)
                    shutil.copy(item.path, destination)
    except IOError:
        print("Problem reading listfile")


parser = argparse.ArgumentParser(description = "arguments for filtering OGs to only those with a given number of taxa")
parser.add_argument("-l", "--listfile", required = True, help = "list of desired OG names")
parser.add_argument("-a", "--aligndir", required = True, help = "path to a directory with alignments in it")
parser.add_argument("-n", "--newdir", required = True, help = "path to a directory for the desired alignments")
args = parser.parse_args()

pull_info_files()
