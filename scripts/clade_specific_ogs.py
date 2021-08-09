#! /usr/bin/env python3

#function to identify all of the orthogroups that contain only those species from a specific clade,
#provided as a list of species.

#still needs some troubleshooting, especially at the loop break point

import argparse
import os
import Bio.SeqIO
import re

def identify_ogs():

    #create a set of all the members of the clade of interest
    clade = set()

    try:
        with open("{0}".format(args.listfile), "r") as inlist:
            with open("{0}".format(args.output), "w") as outlist:
                for line in inlist:
                    species_name = line.strip()
                    clade.add(species_name)

            #scan through all the files in the fasta directory, and pull out the genus name
            for file in os.scandir("{0}".format(args.directory)):
                for record in Bio.SeqIO.parse("{0}".format(file.path), "fasta"):
                    og_name = re.match("(OG\d+)\.fa", "{0}".format(file.path))
                    taxon_name = re.match(">(\w+)_\w+_\d+", "{0}".format(record.id))
                    if not taxon_name.group(1) in clade:
                        break
                    if taxon_name.group(1) in clade:
                        continue

                    outlist.write("{0}\n".format(og_name.group(1)))

    except IOError:
        print("Issue reading or writing file")

parser = argparse.ArgumentParser(description = "Arguments for extracting clade-specific orthogroups")
parser.add_argument("-l", "--listfile", help = "path to input list of organisms in a clade of interest")
parser.add_argument("-d", "--directory", help = "path to a directory that contains fasta files")
parser.add_argument("-o", "--output", help = "path to an outputted list file with all the orthogroup names")
args = parser.parse_args()
