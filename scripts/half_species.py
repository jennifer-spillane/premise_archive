#! /usr/bin/env python3

import argparse

def spec_trim():
    try:
        with open("{0}".format(args.matrix), "r") as mfile:
            with open("{0}".format(args.output), "w") as outfile:
                for line in mfile:
                    if line.startswith("Orthogroup"):
                        outfile.write(line)
                    else:
                        spec_count = 0
                        og_info = line.split("\t")
                        for item in og_info[1:]:
                            if item == "1":
                                spec_count += 1
                        if spec_count >= args.count:
                            og_line = "\t".join(og_info)
                            outfile.write(og_line)
    except IOError:
        print("Issue reading or writing file")



parser = argparse.ArgumentParser(description = "arguments for orthogroup matrix trimming")
parser.add_argument("-m", "--matrix", required = True, help = "orthogroup matrix to trim")
parser.add_argument("-o", "--output", required = True, help = "trimmed matrix output file")
parser.add_argument("-c", "--count", type = int, required = True, help = "number of species necessary to keep orthogroup")
args = parser.parse_args()

spec_trim()

#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/half_species.py
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/cor_pres_abs.txt
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/output_half_species.csv

#on 11/9/18 when I run it on my matrix with 67 taxa and a count of 33, I get 6285 orthogroups
