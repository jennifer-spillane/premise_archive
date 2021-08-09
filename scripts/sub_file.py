#! /usr/bin/env python3

#A script to subsample a file by lines

import argparse

def sub_file():
    count = 0
    try:
        with open("{0}".format(args.infile), "r") as depth_file:
            with open("{0}".format(args.outfile), "w") as output:
                for line in depth_file:
                    count += 1
                    if count % int(args.number) == 0:
                        output.write("{0}".format(line))
    except IOError:
        print("Issue reading file")

parser = argparse.ArgumentParser(description = "arguments for subsampling files to take only every nth line")
parser.add_argument("-i", "--infile", required = True, help = "Any file split up by lines")
parser.add_argument("-o", "--outfile", required = True, help = "name of file to write the new subsampled data")
parser.add_argument("-n", "--number", type = int, required = True, help = "provide it with 'n', the number of lines to skip")
args = parser.parse_args()

sub_file()
