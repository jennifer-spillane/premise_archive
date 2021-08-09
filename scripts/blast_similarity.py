#! /usr/bin/env python3

import argparse

def parse_blast():
    #list to hold the blast results with 97% similarity or higher
    good_results = []
    #list to hold the matching go term results
    go_matches = []
    #this section parses through the blast output file and adds lines of it to a list if they meet the threshold
    try:
        with open("{0}".format(args.input), "r") as infile:
            for line in infile:
                fields = line.split("\t") #a list containing all of the blast output info
                similarity = float(fields[3].strip())
                if similarity >= 97.0:
                    good_results.append(fields[6].strip())
    except(IOError):
        print("Issue reading input file")

    #this section goes through the go file (a tsv generated with interproscan) and finds the lines that match those good hits from the previous step
    try:
        with open("{0}".format(args.gofile), "r") as go_info:
            for thing in go_info:
                gofields = thing.split("\t")
                for item in good_results:
                    if item.strip() == gofields[0].strip():
                        go_matches.append(thing)
    except(IOError):
        print("Issue reading GO file")

    #here we're just writing to a new outfile
    try:
        with open("{0}".format(args.output), "w") as outfile:
            for match in go_matches:
                outfile.write("{0}".format(match))
    except(IOError):
        print("Issue writing output file")


parser = argparse.ArgumentParser(description = "arguments for finding the right mouse transcripts")
parser.add_argument("-i", "--input", required = True, help = "path to blast output in format 6")
parser.add_argument("-g", "--gofile", required = True, help = "path to interproscan tsv output")
parser.add_argument("-o", "--output", required = True, help = "path to an output tsv file")
args = parser.parse_args()

parse_blast()
