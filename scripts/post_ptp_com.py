#! /usr/bin/env python3

# a script to compare the contents of orthogroups (post-phylotreepruner) to one another in different datasets

import argparse
import re
import os



def postcom():
    #setting up the dictionary that will hold all the set information
    db_trans_sets = dict()

    #making lists of the files contained in the directories
    dir1_set = set(os.listdir("{0}".format(args.directory1)))
    dir2_set = set(os.listdir("{0}".format(args.directory2)))
    dir3_set = set(os.listdir("{0}".format(args.directory3)))

    #finding the mouse transcripts that they all have in common
    common_dir1_dir2 = dir1_set.intersection(dir2_set)
    common_files = dir3_set.intersection(common_dir1_dir2)

    #checking to see that the files are the right ones and making the mouse transcripts the keys in the top dictionary
    for item in common_files:
        if item.startswith("Mus"):
            if not item.endswith("_rename"):
                db_trans_sets[item] = dict()

                #going through each directory and populating the dictionary with the correct keys and values
                #starting with directory 1
                for entry1 in os.scandir("{0}".format(args.directory1)):
                    if entry1.name == item:
                        db_trans_sets[item].setdefault(args.directory1, set())
                        try:
                            with open("{0}".format(entry1.path), "r") as data1:
                                for line1 in data1:
                                    if line1.startswith(">"):
                                        stripped1 = line1.strip()
                                        db_trans_sets[item][args.directory1].add(stripped1)
                        except IOError:
                            print("something happened while trying to open a file in directory1")

                #now directory 2
                for entry2 in os.scandir("{0}".format(args.directory2)):
                    if entry2.name == item:
                        db_trans_sets[item].setdefault(args.directory2, set())
                        try:
                            with open("{0}".format(entry2.path), "r") as data2:
                                for line2 in data2:
                                    if line2.startswith(">"):
                                        stripped2 = line2.strip()
                                        db_trans_sets[item][args.directory2].add(stripped2)
                        except IOError:
                            print("something happened while trying to open a file in directory2")

                #now directory 3
                for entry3 in os.scandir("{0}".format(args.directory3)):
                    if entry3.name == item:
                        db_trans_sets[item].setdefault(args.directory3, set())
                        try:
                            with open("{0}".format(entry3.path), "r") as data3:
                                for line3 in data3:
                                    if line3.startswith(">"):
                                        stripped3 = line3.strip()
                                        db_trans_sets[item][args.directory3].add(stripped3)
                        except IOError:
                            print("something happened while trying to open a file in directory3")


    #Now on to the comparing part, and calculating intersectionality
    for mouse_trans in db_trans_sets:
        #make new sets that contain the sets from the dictionary - just to make them shorter to access
        set1 = db_trans_sets[mouse_trans][args.directory1]
        set2 = db_trans_sets[mouse_trans][args.directory2]
        set3 = db_trans_sets[mouse_trans][args.directory3]

        #print("the set of transcripts for mouse transcript {0} is {1}".format(mouse_trans, set1))
        jac_1and2 = (len(set1.intersection(set2))) / (len(set1.union(set2)))
        #print(jac_1and2)
        print("length of the intersection: {0} divided by the length of the union: {1} = {2}".format(len(set1.intersection(set2)), len(set1.union(set2)), jac_1and2))









parser = argparse.ArgumentParser(description = "arguments for comparing the identity of OGs after PhyloTreePruner")
parser.add_argument("-d", "--directory1", required = True, help = "path to directory containing alignment files")
parser.add_argument("-e", "--directory2", required = True, help = "path to directory containing alignment files")
parser.add_argument("-f", "--directory3", required = True, help = "path to directory containing alignment files")
args = parser.parse_args()

postcom()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/post_ptp_compare.py
#/mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/bad/for_orthofinder/Results_May22/Orthologues_May22/pruned/toy_data/
#/mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/good/for_orthofinder/Results_May22/Orthologues_May22/pruned/toy_data/
#/mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/trin/for_orthofinder/Results_May23/Orthologues_May24/pruned/toy_data/
#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/post_ptp_compare.py -d /mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/bad/for_orthofinder/Results_May22/Orthologues_May22/pruned/toy_data/ -e /mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/good/for_orthofinder/Results_May22/Orthologues_May22/pruned/toy_data/ -f /mnt/lustre/macmaneslab/jlh1023/phylo_qual/second_test/trin/for_orthofinder/Results_May23/Orthologues_May24/pruned/toy_data/
