#! /usr/bin/env python3

#A script to count the number of sequences each taxon has in all the orthogroups
#OrthoFinder calculates this, but since I have filtered down the orthogroups, those numbers are no longer accurate.


import argparse
import os
import Bio.SeqIO
import re


def ortho_stat():
    #make a dictionary to hold the species names and how many times they occur
    species_counts = {}
    passing_files = []

    #scan through the directory with all of the clean orthogroup fastas
    for file in os.scandir("{0}".format(args.directory)):

        #only interested in the cleaned orthogroup files
        if file.name.endswith("clean"):

            #creating a list to hold all the protein seqs in each fasta, to check how many there are
            prots = []
            try:
                #checking to see if the orthogroup file has at least two sequences in it
                for record in Bio.SeqIO.parse("{0}".format(file.path), "fasta"):
                    prots.append(record.id)

                #only moving on to the next steps if there are at least two sequences in the orthogroup file
                if len(prots) >= 2:
                    passing_files.append(file.path)

            except IOError:
                print("Problem reading file")

    try:
        for item in passing_files:
            for sequence in Bio.SeqIO.parse("{0}".format(item), "fasta"):
                species_name = re.match("([A-z]+_[a-z]+)_\d+", "{0}".format(record.id))
                species_counts.setdefault(species_name.group(1), 0)
                #if
                species_counts[species_name.group(1)] += 1
                #species_counts[species_name.group(1)] = species_counts[species_name.group(1)] + 1

    except IOError:
        print("Problem reading fasta")

    try:
        with open("{0}".format(args.output), "w") as outfile:
            for entry in species_counts:
                outfile.write("{0}\t{1}\n".format(entry, species_counts[entry]))
    except IOError:
        print("Issue writing file")


parser = argparse.ArgumentParser(description = "arguments for filtering orthogroups down to one sequence each")
parser.add_argument("-d", "--directory", required = True, help = "path to directory containing clean orthogroup files")
parser.add_argument("-o", "--output", required = True, help = "name of output file")
args = parser.parse_args()

ortho_stat()

# /mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/ortho_stats.py
# /mnt/lustre/macmaneslab/jlh1023/chap3_2020/alien_indexing/orthogroups
# /mnt/lustre/macmaneslab/jlh1023/chap3_2020/alien_indexing/filtered_species_counts.tsv
