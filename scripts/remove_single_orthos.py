#! /usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--infile", required = True, help = "file to be filtered")
parser.add_argument("-o", "--outfile", required = True, help = "output filename")
args = parser.parse_args()

try:
    with open("{0}".format(args.infile), "r") as orig:
        with open("{0}".format(args.outfile), "w") as new:
            for line in orig:
                num_list = []
                components = line.split("\t")
                if components[0] == "#cluster_id":
                    new.write(line)
                else:
                    for item in components[1:]:
                        num_list.append(int(item))
                    if sum(num_list) >= 2:
                        new.write(line)
except IOError:
    print("Problem reading file")
