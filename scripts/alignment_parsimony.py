#! /usr/bin/env python3

import argparse
import os
import re

def alignment_parsimony():
    try:
        sites = ""
        with open("{0}".format(args.outfile), "w") as out_file:
            for file in os.scandir("{0}".format(args.indir)):
                if file.name.endswith("iqtree"):
                    with open("{0}".format(file.path), "r") as infile:
                        for jumble in infile:
                            if jumble.startswith("Input data"):
                                data = jumble.strip()
                                sites = re.match("Input data: 39 sequences with (\d+) amino-acid sites", "{0}".format(data))
                            if jumble.startswith("Number of parsimony informative sites:"):
                                line = jumble.strip()
                                count = re.match("Number of parsimony informative sites: (\d+)", "{0}".format(line))

                                percentage = (int(count.group(1)) / int(sites.group(1)))
                                if percentage:
                                    out_file.write("{0}\t{1}\n".format(file.name, str(percentage)))
    except IOError:
        print("problem reading or writing file")

parser = argparse.ArgumentParser(description = "arguments for pulling out constant numbers from alignment info files")
parser.add_argument("-i", "--indir", required = True, help = "path to directory with iqtree info files")
parser.add_argument("-o", "--outfile", required = True, help = "output file name")
args = parser.parse_args()

alignment_parsimony()
