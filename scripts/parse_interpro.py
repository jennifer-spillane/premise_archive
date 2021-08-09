#! /usr/bin/env python3

import argparse

#a function to process the tsv file out of interproscan

def intermouse():
    mouse_go = dict() #dictionary with mouse transcripts and GO terms for the whole transcriptome
    all_gos = []
    mouse_trans = [] #list of mouse transcripts of interest
    select_gos = []
    try:
        #formatting the tsv file correctly
        #pulling out the transcript names as keys and the GO terms as values in a dictionary
        with open("{0}".format(args.inter)) as infile:
            for line in infile:
                stripped = line.strip()
                fields = stripped.split("\t")
                mouse_go.setdefault(fields[0], [])
                if len(fields) > 13:
                    gos = fields[13].split("|")
                    for item in gos:
                        #mouse_go.setdefault(fields[0], [])
                        mouse_go[fields[0]].append(item)
                        all_gos.append(item)
                else:
                    continue

        with open("mouse_ref_terms.txt", "w") as ref_file:
            for thing in all_gos:
                ref_file.write("{0}\n".format(thing))

        #reading the list of transcripts of interest, and pulling out the go terms associated with them
        with open("{0}".format(args.listfile), "r") as list_file:
            for line in list_file:
                just_trans = line.strip()
                mouse_trans.append(just_trans)
            for transcript in mouse_trans:
                if transcript in mouse_go:
                    for go in mouse_go[transcript]:
                        select_gos.append(go)

        #writing the new list to a user specified file
        with open("{0}".format(args.out), "w") as outfile:
            for term in select_gos:
                outfile.write("{0}\n".format(term))

    except IOError:
        print("difficulty reading this file")


parser = argparse.ArgumentParser(description = "arguments for finding the functions of specific mouse transcripts")
parser.add_argument("-i", "--inter", required = True, help = "path to interproscan tsv output")
parser.add_argument("-l", "--listfile", required = True, help = "path to a list file of all transcripts of interest")
parser.add_argument("-o", "--out", required = True, help = "path to an output text file")
args = parser.parse_args()

intermouse()
