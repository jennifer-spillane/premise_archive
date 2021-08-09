#! /usr/bin/env python3

#a function to pull the gene tree files that correspond to a list of gene trees of interest
#in most cases this will be the shortest ones, but could be anything in a list of gene trees.

import argparse
import os
import shutil

def psgt():
    #creating the dictionary, counter, and list I'll need inside the loop
    #top_ten = {}
    count = 0
    short_set = set()
    #putting all of the numbers of interest into a set for easy comparison
    try:
        with open("{0}".format(args.tree_nums), "r") as shortest:
            print("opened number file")
            for line in shortest:
                tree = line.strip()
                short_set.add(int(tree))
            print("made set of numbers")
            #scanning through the directory of gene trees and finding the ones that match up with the numbers
            #in the list file provided. Copying these trees to a new directory
            for entry in os.scandir("{0}".format(args.tree_dir)):
                count += 1
                destination = os.path.join(args.new_dir, entry.name)
                #top_ten.setdefault(count, entry.path)
                if count in short_set:
                    shutil.copy(entry.path, destination)
    except IOError:
        print("problem reading file")


parser = argparse.ArgumentParser(description = "arguments for filtering OGs to only those with a given number of taxa")
parser.add_argument("-t", "--tree_nums", required = True, help = "list of gene tree numbers of interest")
parser.add_argument("-d", "--tree_dir", required = True, help = "path to a directory with gene trees in it")
parser.add_argument("-n", "--new_dir", required = True, help = "path to a directory for the desired gene trees")
args = parser.parse_args()

psgt()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/pull_short_gene_trees.py \
#-t /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/bad/trees/top_ten_percent.txt \
#-d /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/bad/trees/gene_trees \
#-n /mnt/lustre/macmaneslab/jlh1023/phylo_qual/actual_final/bad/trees/short_gene_trees
