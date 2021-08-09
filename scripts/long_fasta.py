#! /usr/bin/env python3

import Bio.SeqIO
import argparse

# a script to extract only contigs above a certain length from a fasta file.

def long_fasta():
    try:
        rec_list = []
        for record in Bio.SeqIO.parse("{0}".format(args.in_fasta), "fasta"):
            print("{0}".format(len(record.seq)))
            if len(record.seq) >= args.length:
                rec_list.append(record)
        Bio.SeqIO.write(rec_list, "{0}".format(args.out_fasta), "fasta")
    except IOError:
        print("Issue reading file")

parser = argparse.ArgumentParser(description = "Arguments for taking long contigs")
parser.add_argument("-i", "--in_fasta", help = "path to input fasta file")
parser.add_argument("-o", "--out_fasta", help = "path to output fasta file")
parser.add_argument("-l", "--length", type = int, help = "shortest acceptable contig length")
args = parser.parse_args()

long_fasta()
