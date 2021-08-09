#! /usr/bin/env python3

#A script to filter orthogroup sequences down to just a single representative sequence per orthogroup.
#First, it eliminates orthogroups that only contain 1 (or don't contain any) sequence (from a previous filtering step).
#Second, it runs usearch cluster_fast using size as the input order to find centroid sequences that are also relatively long.
#Third, it filters the centroids and chooses the one that represents the most sequences.
#If there are two or more sequences that tie, it will take the first one, which should also be the longest.

import argparse
import os
import Bio.SeqIO
import subprocess
import re

def filter_clust():
    #make a list to hold the representative sequence records for each orthogroup
    good_seq_list = []

    #scan through the directory with all of the clean orthogroup fastas
    for file in os.scandir("{0}".format(args.directory)):
        #creating variables that correspond to the name of the sequence with the largest cluster,
        #the line that will be the header for that sequence in the new fasta file, and
        #the sequence that will go with that header
        biggest_clust = ""
        fasta_header = ""
        fasta_seq = ""

        #only interested in the cleaned orthogroup files
        if file.name.endswith("clean"):
            #isolating the orthogroup name to be used later in file names and headers, and printing it for the log file
            base_name = re.match("(OG\d+)", "{0}".format(file.name))
            print(base_name.group(1))
            #creating a list to hold all the protein seqs in each fasta, to check how many there are
            prots = []
            try:
                #checking to see if the orthogroup file has at least two sequences in it
                for record in Bio.SeqIO.parse("{0}".format(file.path), "fasta"):
                    prots.append(record.id)
                #printing the number of proteins in the list for the log file
                print(len(prots))

                #only moving on to the next steps if there are at least two sequences in the orthogroup file
                if len(prots) >= 2:
                    #clustering with usearch using sequence length as the input order
                    subprocess.run("usearch -cluster_fast {0} -sort length -id 0.6 -centroids {1}_cent.fa -uc {1}.uc ".format(file.path, base_name.group(1)), shell = True)

                    #open the relevant output files from the usearch command above
                    with open("{0}.uc".format(base_name.group(1)), "r") as countfile:
                        #creating a list to hold tuples of cluster info
                        clusters = []
                        #in the tab-delimited file, we are only interested in the lines labelled "C" as these are the clusters
                        for line in countfile:
                            fields = line.split("\t")
                            if fields[0] == "C":
                                #we want the sequence name from the 9th field and the size of the cluster
                                #from the 3rd field, saved in a tuple in the list
                                seq_name = fields[8].strip()
                                clust_size = int(fields[2].strip())
                                clusters.append((seq_name, clust_size))
                        #finding the largest cluster in the list of tuples
                        biggest_clust = max(clusters, key = lambda item: item[1])[0]
                        #creating the header of the fasta for this  seq with the largest cluster and printing for the log file
                        fasta_header = "{0}_{1}".format(base_name.group(1), biggest_clust)
                        print(fasta_header)

                        #now we go into the file of centroids from usearch, and find the sequence that matches the largest cluster seq name
                        for record in Bio.SeqIO.parse("{0}_cent.fa".format(base_name.group(1)), "fasta"):
                            if record.id == biggest_clust:
                                fasta_seq = record.seq
                    #creat a SeqRecord out of all the relevant info, and append to the list of good sequences
                    good_record = Bio.SeqRecord.SeqRecord(id = fasta_header, seq = fasta_seq, description = "")
                    good_seq_list.append(good_record)

            except IOError:
                print("Problem reading file")

    #write out the final fasta file with all the representative sequences for each orthogroup
    Bio.SeqIO.write(good_seq_list, "rep_og_seqs.fa", "fasta")


parser = argparse.ArgumentParser(description = "arguments for filtering orthogroups down to one sequence each")
parser.add_argument("-d", "--directory", required = True, help = "path to directory containing clean orthogroup files")

args = parser.parse_args()

filter_clust()

# /mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/clust_wrapper.py
# /mnt/lustre/macmaneslab/jlh1023/chap3_2020/alien_indexing/orthogroups
