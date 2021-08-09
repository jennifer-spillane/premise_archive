#! /usr/bin/env python3

import os
import re
import argparse

#function to store the names of the species and associate them with their accessions.
def names():
    species_db = {}
    for entry in os.scandir("{0}".format(args.transcripts)):
        try:
            with open("{0}".format(entry.path)) as fasta_file:
                first_line = fasta_file.readline()
                #isolate species name without the rest of the header
                species = re.search("TSA:.([A-Z][a-z]+.[a-z]+)", first_line)
                species_name = species.group(1)
                species_name = species_name.replace(" ", "_")
                #isolate file name without .fasta
                acc_name = entry.name[0:6]
                #add these to the dictionary
                species_db[acc_name] = species_name
        except IOError:
            print("Problem reading file")
    return species_db



parser = argparse.ArgumentParser(description = "Arguments for the final project pipeline")
parser.add_argument("transcripts", help = "path to a directory containing the transcriptomic datasets")
args = parser.parse_args()

names()
