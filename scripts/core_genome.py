#! /usr/bin/env python3

import argparse

def core():
    try:
        with open("{0}".format(args.matrix), "r") as infile:
            with open("{0}".format(args.output), "w") as outfile:
                for line in infile:
                    if not line.startswith("#cluster_id"):
                        stripped = line.strip()
                        og_info = stripped.split("\t")
                        pres = set(og_info[1:])
                        if len(pres) == 1:
                            outfile.write("{0}\n".format(og_info[0]))
    except IOError:
        print("Issue reading/writing files")


parser = argparse.ArgumentParser(description = "arguments for finding the core genome of a clade")
parser.add_argument("-m", "--matrix", required = True, help = "matrix file of presence and absense of orthogroups")
parser.add_argument("-o", "--output", required = True, help = "path to output file")
args = parser.parse_args()

core()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/core_genome.py
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/output_half_species.csv
