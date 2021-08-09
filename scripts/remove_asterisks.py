#! /usr/bin/env python3
#accepts a directory and looks into each file to make sure that there are no
#asterisks present. These will mess up interproscan.

import argparse
import os

def asterisk():
    for entry in os.scandir("{0}".format(args.directory)):
        if entry.is_file():
            try:
                with open("{0}".format(entry.path), "r") as fasta_file:
                    #print("opened file")
                    with open("temp_file.fasta", "w") as new_file:
                        all_lines = ""
                        for line in fasta_file:
                            line_new = line.replace("*", "")
                            all_lines += line_new
                        new_file.write(all_lines)
                    os.rename("temp_file.fasta", "{0}".format(entry.path))
            except IOError:
                print("problem reading file")

parser = argparse.ArgumentParser()
parser.add_argument("directory", help = "path to a directory containing the protein fastas")
args = parser.parse_args()

asterisk()
