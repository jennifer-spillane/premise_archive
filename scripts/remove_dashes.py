#! /usr/bin/env python3
#accepts a file and looks at each sequence to make sure that there are no
#dashes present. These will mess up interproscan.

#the files I have been working with went through a program that wraps the sequence lines in a way that I hate.
#I have used this awk command to fix this:
#awk '{if(NR==1) {print $0} else {if($0 ~ /^>/) {print "\n"$0} else {printf $0}}}' bad_mus_unique.fasta > fixed_bad_mus_unique.fasta

import argparse
import os

def dashes():
    try:
        with open("{0}".format(args.input), "r") as fasta_file:
            print("opened file")
            with open("temp_file.fasta", "w") as new_file:
                all_lines = ""
                for line in fasta_file:
                    line_new = line.replace("-", "")
                    all_lines += line_new
                new_file.write(all_lines)
            os.rename("temp_file.fasta", "{0}".format(args.output))
    except IOError:
        print("problem reading file")

parser = argparse.ArgumentParser(description = "Arguments for taking long contigs")
parser.add_argument("-i", "--input", help = "path to input directory full of alignment files")
parser.add_argument("-o", "--output", help = "path to output fasta file")
args = parser.parse_args()

dashes()
