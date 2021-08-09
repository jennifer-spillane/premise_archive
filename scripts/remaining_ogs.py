#! /usr/bin/env python3
#a function to identify all the orthogroups that have not been run yet in the dollo_model.py script
#it takes the remaining OGs and puts them into a new matrix file that can be run separately
#sort of "resets" the process to fix any nodes that might be hung up on long or impossible OGs.

#############################
#bash stuff I did ahead of time - all happening in this directory:
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling
###################################

##extract the names of the OGs that have already been processed and are present in the results file
##sort them and send them to a new file
#cut -f 1 half_species_results.csv | sort > processed.txt

##extract the names of the OGs in the original file that was fed into the program
##sort them and send them to a new file
#cut -f 1 ../Results_Jul17/output_half_species.csv | sort > orig_ogs.txt

##compare the two groups and retain the ones that are only present in the
##original file (the ones that have not been processed)
#comm -23 orig_ogs.txt processed.txt > leftover.txt

############################
#and now the python script to pull the ogs in the file "leftover.txt" into a new file with all of their info
##########################

import argparse

def trouble():
    leftover_ogs = set()
    try:
        with open("{0}".format(args.leftover), "r") as left_file:
            for line in left_file:
                stripped = line.strip()
                leftover_ogs.add(stripped)
        with open("{0}".format(args.matrix), "r") as mfile:
            with open("{0}".format(args.output), "a") as outfile:
                for line in mfile:
                    if line.startswith("#cluster_id"):
                        outfile.write(line)
                    else:
                        stripped = line.strip()
                        og_info = stripped.split("\t")
                        for num in leftover_ogs:
                            if og_info[0] == num:
                                outfile.write(line)

    except IOError:
        print("Don't screw this up")

parser = argparse.ArgumentParser(description = "arguments for pulling out the slower ogs")
parser.add_argument("-m", "--matrix", required = True, help = "matrix file of presence and absense of orthogroups")
parser.add_argument("-l", "--leftover", required = True, help = "file with leftover og numbers one per line")
parser.add_argument("-o", "--output", required = True, help = "path to output file")
args = parser.parse_args()

trouble()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/remaining_ogs.py
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/output_half_species.csv
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling/leftover.txt
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling/leftovers_results.csv

###################################
##check to see that it worked and you have no repeats:
#cut -f 1 leftovers_results.csv | sort > checking.txt
#comm processed.txt checking.txt > comm_file.txt

##in this file there should be things in the first two columns, but not the third

##if you want to check that the ogs that you pulled out to restart the run are indeed the
##ones that you put into your leftover.txt file, you can comm that as well
#comm checking.txt leftover.txt > comm_file.txt

##in this file there should be only stuff in the third column

#######################################
##after running this script, you'll also need to run one to add the two results files together
##this line removes the first line of the leftover results file:
#sed -i '1d' leftovers_results.csv

##then just cat them together:
#cat original_results.csv leftovers_results.csv > new_file.csv

##And then you should be good!
