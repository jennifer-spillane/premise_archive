#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser(description = "arguments for finding interesting OGs")
parser.add_argument("-i", "--input", required = True, help = "Path to the spreadsheet to be analyzed")
args = parser.parse_args()

try:
    with open("{0}".format(args.input), "r") as og_file:
        print("opened file")
        for line in og_file:
            if line.startswith("OG"):
                nodes = line.split("\t")
                if float(nodes[3]) <= 0.2:
                    #print("found all low sponge nodes")
                    if float(nodes[9]) >= 0.7:
                        if float(nodes[16]) >= 0.7:
                            loss = "\t".join(nodes)
                            print(loss)
except IOError:
    print("Problem reading file")


#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/parse_dollo_results.py
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/modeling/one_k_results.csv
