#! /usr/bin/env python3

import argparse
import os
import re

def alignment_composition():
    try:
        length = ""
        with open("{0}".format(args.outfile), "w") as out_file:
            for file in os.scandir("{0}".format(args.indir)):
                if file.name.endswith("phylip.log"):
                    with open("{0}".format(file.path), "r") as infile:
                        for jumble in infile:
                            if jumble.startswith("Alignment has 39 sequences with"):
                                data = jumble.strip()
                                length = re.match("Alignment has 39 sequences with (\d+) columns, \d+ distinct patterns", "{0}".format(data))
                            if jumble.startswith("****  TOTAL"):
                                line = jumble.strip()
                                percentage = re.match("\*\*\*\*  TOTAL           [0-9]+\.*[0-9]*%  ([0-9]+) sequences failed composition chi2 test", "{0}".format(line))
                                if percentage:
                                    out_file.write("{0}\t{1}\t{2}\n".format(file.name, length.group(1), percentage.group(1)))
                                else:
                                    out_file.write("{0}\t{1}\t0\n".format(file.name, length.group(1)))
    except IOError:
        print("problem reading or writing file")

parser = argparse.ArgumentParser(description = "arguments for pulling out constant numbers from alignment info files")
parser.add_argument("-i", "--indir", required = True, help = "path to directory with iqtree log files")
parser.add_argument("-o", "--outfile", required = True, help = "output file name")
args = parser.parse_args()

alignment_composition()
