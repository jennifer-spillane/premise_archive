#! /usr/bin/env python3

import argparse

def depth_file_parsing():
    count = 0
    try:
        with open("{0}".format(args.input), "r") as infile:
            with open("{0}".format(args.output), "w") as outfile:
                for contig in infile:
                    stripped = contig.strip()
                    fields = stripped.split("\t")
                    if int(fields[2]) >= args.depth_threshold:
                        outfile.write(contig)
                        count += 1
                print("Number of contigs with depth at or over {0}: {1}".format(args.depth_threshold, count))

    except IOError:
        print("Issue reading file")

parser = argparse.ArgumentParser(description = "arguments for parsing a depth file")
parser.add_argument("-i", "--input", required = True, help = "the output of a samtools depth command")
parser.add_argument("-o", "--output", required = True, help = "name of file to write the lines containing deep-sequenced contigs")
parser.add_argument("-d", "--depth_threshold", type = int, required = True, help = "cutoff of depth you are interested in")
args = parser.parse_args()

depth_file_parsing()
