#! /usr/bin/env python3

#script takes in a list of unwanted seq names and an interproscan output tsv file.
#removes seq results that correspond to the list of names and outputs a clean file without them.

import argparse

def prune():

    #make a set to hold the unwanted sequences
    #make a list to hold the lines of the tsv file that pass inspection
    wanted_seqs = set()
    clean_tsv_lines = []

    try:
        with open("{0}".format(args.listfile), "r") as inlist:
            with open("{0}".format(args.tsvfile), "r") as interfile:
                #add all the unwanted seq names to the set
                for seq in inlist:
                    prot_name = seq.strip()
                    wanted_seqs.add(prot_name)

                #isolate the relevant part of the interproscan file
                for line in interfile:
                    fields = line.split("\t")
                    name = fields[0].strip()
                    #test against the seq names in the set and append to the list if it isn't in the set
                    if name in wanted_seqs:
                        clean_tsv_lines.append(line)
                    else:
                        continue

        #open a new file and add the lines that passed the test to it.
        with open("{0}".format(args.outtsv), "w") as outfile:
            for entry in clean_tsv_lines:
                outfile.write("{0}".format(entry))
    except IOError:
        print("Problem reading or writing file")


parser = argparse.ArgumentParser(description = "Arguments for pruning alien sequences out of interproscan results")
parser.add_argument("-l", "--listfile", help = "path to input list of sequences that are wanted in interproscan results")
parser.add_argument("-t", "--tsvfile", help = "path to a tsv file that interproscan outputs")
parser.add_argument("-o", "--outtsv", help = "path to a new output tsv file without the unwanted entries")
args = parser.parse_args()

prune()


#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/prune_interpro_results.py
