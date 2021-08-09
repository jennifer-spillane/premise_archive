#! /usr/bin/env python3

#a function to pull the gene tree files that correspond to a list of gene trees of interest
#could be anything of interest in a list of gene trees.
#this script pulls gene trees based on identity number, but pull_short_gene_trees.py will work on order number within the directory

import argparse
import os
import shutil
import re

def psgt():
    #creating the set I'll need inside the loop
    certain_set = set()
    #putting all of the numbers of interest into a set for easy comparison
    try:
        with open("{0}".format(args.tree_nums), "r") as interesting:
            print("opened interesting gene tree num file")
            for line in interesting:
                tree = line.strip()
                certain_set.add(tree)
            print("made set of gene tree nums")
            try:
                os.mkdir("{0}".format(args.new_dir))
            except FileExistsError:
                print("This directory already exists. Please provide a different name")
            #scanning through the directory of gene trees and finding the ones that match up with the numbers
            #in the list file provided. Copying these trees to a new directory
            for item in os.scandir("{0}".format(args.tree_dir)):
                just_name = re.match("(Mus_musculus\|\d+_rename)\.phylip\.treefile", "{0}".format(item.name))
                if just_name.group(1) in certain_set:
                    #copy the ones that match into the directory you made earlier
                    destination = os.path.join(args.new_dir, item.name)
                    shutil.copy(item.path, destination)

    except IOError:
        print("problem reading file")


parser = argparse.ArgumentParser(description = "arguments for filtering OGs to only those with a given number of taxa")
parser.add_argument("-t", "--tree_nums", required = True, help = "list of gene tree numbers of interest")
parser.add_argument("-d", "--tree_dir", required = True, help = "path to a directory with gene trees in it")
parser.add_argument("-n", "--new_dir", required = True, help = "path to a directory for the desired gene trees")
args = parser.parse_args()

psgt()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/pull_certain_gene_trees.py \
#-t /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/comparisons/common_to_both.txt \
#-d /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/good/trees/gene_trees/ \
#-n /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/good/trees/good_common_gene_trees/
