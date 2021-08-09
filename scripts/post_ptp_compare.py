#! /usr/bin/env python3

# a script to compare the contents of orthogroups (post-phylotreepruner) to one another in different datasets

import argparse
import re
import os
import shutil


def postcom():
    #setting up the dictionary that will hold all the set information
    db_trans_sets = dict()

    #making lists of the files contained in the directories
    dir1_list = os.listdir("{0}".format(args.directory1))
    dir2_list = os.listdir("{0}".format(args.directory2))
    dir3_list = os.listdir("{0}".format(args.directory3))

    #going through the first directory, opening the correct files
    for entry in os.scandir("{0}".format(args.directory1)):
        if entry.name.startswith("Mus"):
            if not entry.name.endswith("_rename"):
                #populating the dictionary with another dictionary to hold the dataset information and the sets
                db_trans_sets[entry.name] = dict()
                db_trans_sets[entry.name][args.directory1] = set()
                try:
                    #finding the correct lines to put into the set and populating it.
                    with open("{0}".format(entry.path), "r") as data1:
                        for line in data1:
                            if line.startswith(">"):
                                stripped = line.strip()
                                db_trans_sets[entry.name][args.directory1].add(stripped)
                except IOError:
                    print("problem opening file")

                #grabbing the ones from dir 2
                dir2_file = os.path.join(args.directory2, entry.name)
                if entry.name in dir2_list:
                    try:
                        with open("{0}".format(dir2_file), "r") as same_in_dir2:
                            for line in same_in_dir2:
                                if line.startswith(">"):
                                    stripped = line.strip()
                                    db_trans_sets[entry.name].setdefault(args.directory2, set())
                                    db_trans_sets[entry.name][args.directory2].add(stripped)
                    except IOError:
                        print("try it again")

                #grabbing the ones from dir 3
                dir3_file = os.path.join(args.directory3, entry.name)
                if entry.name in dir3_list:
                    try:
                        with open("{0}".format(dir3_file), "r") as same_in_dir3:
                            for line in same_in_dir3:
                                if line.startswith(">"):
                                    stripped = line.strip()
                                    db_trans_sets[entry.name].setdefault(args.directory3, set())
                                    db_trans_sets[entry.name][args.directory3].add(stripped)
                    except IOError:
                        print("we've been through this")

    #what if the transcript is in dir 2, but not 1?
    for item in dir2_list:
        item_file = os.path.join(args.directory2, item)
        if item.startswith("Mus"):
            if not item.endswith("_rename"):
                if not item in db_trans_sets.keys():
                    db_trans_sets[item] = dict()
                    db_trans_sets[item][args.directory2] = set()
                    try:
                        #finding the correct lines to put into the set and populating it.
                        with open("{0}".format(item_file), "r") as leftovers1:
                            for line in leftovers1:
                                if line.startswith(">"):
                                    stripped = line.strip()
                                    db_trans_sets[item][args.directory2].add(stripped)
                    except IOError as e:
                        print("issue opening file:", e)

                    #what if the thing is in dirs 2 and 3 but not 1?
                    if item in dir3_list:
                        item_dir3_file = os.path.join(args.directory3, item)
                        try:
                            with open("{0}".format(item_dir3_file), "r") as common_dir2_dir3:
                                for trans in common_dir2_dir3:
                                    if trans.startswith(">"):
                                        stripped = trans.strip()
                                        db_trans_sets[item].setdefault(args.directory3, set())
                                        db_trans_sets[item][args.directory3].add(stripped)
                        except IOError:
                            print("2,3 didn't work")

    #what if the transcript is in dir 3 but not 1 or 2?
    for thing in dir3_list:
        thing_file = os.path.join(args.directory3, thing)
        if thing.startswith("Mus"):
            if not thing.endswith("_rename"):
                if not thing in db_trans_sets.keys():
                    db_trans_sets[thing] = dict()
                    db_trans_sets[thing][args.directory3] = set()
                    try:
                        with open("{0}".format(thing_file), "r") as leftovers2:
                            for line in leftovers2:
                                if line.startswith(">"):
                                    stripped = line.strip()
                                    db_trans_sets[thing][args.directory3].add(stripped)
                    except IOError:
                        print("another problem with a file")



    #Now on to the comparing part, and calculating intersectionality
    for mouse_trans in db_trans_sets:
        set1 = db_trans_sets[mouse_trans][args.directory1]
        #set2 = mouse_trans[args.directory2]
        #set3 = mouse_trans[args.directory3]

        print(set1)



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

#need to:
#scan through each directory, find all the files that end in "_rename"
#for each of these files, look into them and make a set that contains the headers (minus the ">" would be great)
#then populate the dictionary (as I work my way down the for loops) with the keys and the sets



#went through the three directories, found the right files, put these all into a set together
#then I could make the dictionary keys from the set, and then go into each directory individually and populate the
#dictionary with the information matching the mouse transcripts that it got from the set
