#! /usr/bin/env python3

#a scipt to take a transcriptome assembly and discard all those transcripts below
#a threshold equal to some fraction of a standard deviation from the median score

import argparse
import statistics
import Bio.SeqIO

def filter():
    try:
        with open("{0}".format(args.contigs), "r") as con_file:
            name_score = {}
            name_tpm = {}
            low_trans = ""
            #looping through the contig file and populating a dictionary
            #keys = names of transcripts, values = transrate scores
            #sending low scoring lines to a file for examination
            for line in con_file:
                line = line.split(",")
                if line[8] == "score":
                    low_trans += ",".join(line)
                else:
                    name_score[line[0]] = float(line[8])
                    name_tpm[line[0]] = float(line[12])
                    if float(line[8]) <= 0.15:
                        low_trans += ",".join(line)

            #writing the rejected lines to a file
            with open("{0}".format(args.bad_file), "w") as rejected:
                rejected.write(low_trans)

            #finding the median and stddev of all the scores, printing these
            med_score = statistics.median(name_score.values())
            dev_score = statistics.stdev(name_score.values())
            low_bound = med_score - (args.proportion * dev_score)
            print("Median: ", med_score)
            print("Standard Deviation: ", dev_score)
            print("Low Threshold: ", low_bound)

            filtered_list = []
            num_trans = 0
            #looping through the dictionary, populating a new dictionary with transcripts above the threshold
            #recording the number of transcripts retained in the new file
            for entry in name_score:
                if name_score[entry] >= low_bound or name_tpm[entry] >= args.tpm:
                    filtered_list.append(entry)
                    num_trans += 1
            print("Number of transcripts above threshold: ", num_trans)

            transcripts = []
            #looping through both the assembly file and filtered dictionary
            #finding matches and adding them to the new file
            for record in Bio.SeqIO.parse("{0}".format(args.assembly), "fasta"):
                for item in filtered_list:
                    if record.id == item:
                        cur_trans = Bio.SeqRecord.SeqRecord(id = "{0}".format(record.id), seq = record.seq)
                        transcripts.append(cur_trans)

            Bio.SeqIO.write(transcripts, "{0}".format(args.out_fasta), "fasta")
    except IOError:
        print("Issue reading file")



parser = argparse.ArgumentParser(description = "Arguments for filtering transctiptomes")
parser.add_argument("-c", "--contigs", required = True, help = "path to the transrate contigs.csv file")
parser.add_argument("-p", "--proportion", required = True, type = float, help = "proportion of a standard deviation below the median")
parser.add_argument("-o", "--out_fasta", required = True, help = "the name of the new filtered output file")
parser.add_argument("-a", "--assembly", required = True, help = "path to the ORP assembly")
parser.add_argument("-b", "--bad_file", required = True, help = "name of the file with rejected transctripts")
parser.add_argument("-t", "--tpm", required = True, type = float, help = "lowest threshold for tpm")
args = parser.parse_args()

filter()
