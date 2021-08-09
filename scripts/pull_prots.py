#! /usr/bin/env python3

import argparse
import Bio.SeqIO

#function to pull members of one-to-one orthogroups from a protein fasta file
def pull():
    try:
        #creating an empty set and dictionary to hold orthogroups
        ogs = set()
        ols = {}
        prot_set = set()
        with open("{}".format(args.listfile), "r") as list_file:
            with open("{}".format(args.ortho), "r") as ortho_file:
                #saving all the orthogroup names in a set
                for line in list_file:
                    stripped = line.strip()
                    ogs.add(stripped)
                print("Processing {0} OGs".format(len(ogs)))
                #populating the dictionary with keys = orthogroup names,
                #and values = a list of the proteins in that orthogroup
                #also making a set that contains all the protein names
                print("Getting protein names from orthofinder file")
                for line in ortho_file:
                    if line.startswith("OG"):
                        #stripping off white space and splitting on tabs
                        line = line.strip()
                        line = line.split("\t")
                        #if the OG name is in the set, put all the proteins into a new set (and dictionary)
                        if line[0] in ogs:
                            ols.setdefault(line[0], line[1:])
                            for protein in line[1:]:
                                protein = protein.split(", ")
                                for indv in protein:
                                    if indv != "":
                                        prot_set.add(indv)
                print("Pulled {0} protein names from orthofinder file".format(len(prot_set)))

        print("Parsing the fasta file")
        #running through the catted fasta of all the proteins and pulling those seqs that
        #match the ones in the set.
        prot_seqs = []
        prot_names = set()
        for record in Bio.SeqIO.parse("{}".format(args.prots), "fasta"):
            if record.id in prot_set:
                cur_prot = Bio.SeqRecord.SeqRecord(id = record.id, seq = record.seq, description = "")
                cur_prot_name = record.id
                prot_seqs.append(cur_prot)
        Bio.SeqIO.write(prot_seqs, "{}".format(args.out), "fasta")

    except IOError:
        print("Problem reading files")

parser = argparse.ArgumentParser(description = "arguments for pulling 1-to-1 orthologues from a fasta")
parser.add_argument("-l", "--listfile", required = True, help = "all.all.cluster_1to1s.txt provided by kinfin")
parser.add_argument("-r", "--ortho", required = True, help = "Orthogroups.csv provided by orthofinder")
parser.add_argument("-p", "--prots", required = True, help = "fasta file containing all proteins in the orthofinder analysis")
parser.add_argument("-o", "--out", required = True, help = "name of the output fasta file")
args = parser.parse_args()

pull()



#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/pull_prots.py
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/half_species_ogs.txt
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/Orthogroups_4.csv
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/half_species_ogs_all.fasta

#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/sponge_uniq_loss.txt
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/Orthogroups_4.csv
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/interproscan/half_species_ogs_all.fasta
