#! /usr/bin/env python3

import argparse
import os
import re

def tree_length():
    try:
        total = ""
        internal = ""
        with open("{0}".format(args.outfile), "w") as out_file:
            for file in os.scandir("{0}".format(args.indir)):
                if file.name.endswith("iqtree"):
                    with open("{0}".format(file.path), "r") as infile:
                        for jumble in infile:
                            if jumble.startswith("Total tree length"):
                                total_data = jumble.strip()
                                total = re.match("Total tree length \(sum of branch lengths\): (\d+\.*\d*)", "{0}".format(total_data))
                            if jumble.startswith("Sum of internal branch"):
                                internal_data = jumble.strip()
                                internal = re.match("Sum of internal branch lengths: (\d+\.*\d*) \(\d+\.*\d*% of tree length\)", "{0}".format(internal_data))

                                out_file.write("{0}\t{1}\t{2}\n".format(file.name, total.group(1), internal.group(1)))
    except IOError:
        print("problem reading or writing file")

parser = argparse.ArgumentParser(description = "arguments for pulling out constant numbers from alignment info files")
parser.add_argument("-i", "--indir", required = True, help = "path to directory with iqtree info files")
parser.add_argument("-o", "--outfile", required = True, help = "output file name")
args = parser.parse_args()

tree_length()
