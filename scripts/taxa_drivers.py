#! /usr/bin/env python3

import argparse
import os

def taxa_drivers():
    species_counts = {}
    for file in os.scandir("{0}".format(args.alignment_files)):
        #because this script will be happening after the "no_empty_files.py" script,
        #there is no need to filter the files based on name
        try:
            with open("{0}".format(file.path), "r") as infile:
                for line in infile:
                    if line.startswith(">"):
                        stripped = line.strip()
                        #populating the dictionary with species names and initializing counts
                        species_counts.setdefault(stripped, 0)
                        #adding a count for every time it is in a file
                        species_counts[stripped] += 1
        except IOError:
            print("Problem reading the alignment file")
    #writing the final counts to a file
    try:
        with open("{0}".format(args.output), "w") as outfile:
            for entry in species_counts:
                outfile.write("{0}\t{1}\n".format(entry, species_counts[entry]))
    except IOError:
        print("Problem writing to output file")


parser = argparse.ArgumentParser(description = "Arguments for finding the drivers of the OG numbers")
parser.add_argument("-a", "--alignment_files", required = True, help = "directory containing clean alignment files")
parser.add_argument("-o", "--output", required = True, help = "path to output file containing list of taxa and counts")
args = parser.parse_args()

taxa_drivers()
