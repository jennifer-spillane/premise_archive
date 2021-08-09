#! /usr/bin/env python3

import argparse
import os
import re

def normal():
    #setting up an empty dictionary, to hold the genus name as a key and the busco score as a value
    buscos = {}
    og_list = []
    #inside the directory given should be individual directories for each taxon
    #grab the name of the genus to use later from the names of this directory
    for run in os.scandir("{0}".format(args.scores)):
        for thing in os.scandir(run):
            dir_name = re.search("run_(\w+_\w+\.prot).*", run.name)
            gen_name = dir_name.group(1)
            print(gen_name)
            #look into the correct file, find the correct line, and grab the correct characters (the busco score)
            if thing.name startswith("short_summary"):
                try:
                    with open(thing, "r") as score_file:
                        for line in score_file:
                            if line startswith("C:"):
                                perc = line[2-6]
                                print(perc)
                                #populate dictionary with key=genus name and value=busco score
                                buscos.setdefault(gen_name, perc)
    #now opening the matrix file to mess with the scores
    try:
        with open("{0}".format(args.matrix), "r") as matrix_file:
            for line in matrix_file:
                stripped = line.strip()
                fields = stripped.split("\t")
                if fields[0] == "\t":
                    first_line = fields









#script should go find busco scores in a directory given by the user
#take those scores and these numbers of genes from the orthofinder output
#divide the gene numbers by the scores (as a decimal)
#make a new matrix with those adjusted scores
