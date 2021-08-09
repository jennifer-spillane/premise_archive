#! /usr/bin/env python3

import subprocess
import argparse
import os
import shutil
from multiprocessing import Pool, Lock, Value
import threading
import re


def model(og):
    #getting the current thread id
    cur_id = threading.get_ident()

    try:
        master_list = []
        master_tuple = ()
        #making the command to use later
        command = "/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/ace_dollo.r {0}".format(cur_id)
        #split the lines of the matrix and discard the cluster from the first one
        #then write the first line to the new file
        stripped = og[1].rstrip()
        new_stripped = stripped.split("\t")
        og_name = new_stripped[0]
        print("Now working on: {0}".format(og_name))
        #making a set out of the values of the matrix
        #the set will collapse all repeat values
        #so if the length is different from 2, it's universally present or messed up
        #if the line passes, it gets written to the temp file
        sub_stripped = set(new_stripped[1:])
        if len(sub_stripped) == 2:
            with open("{0}_for_r.csv".format(cur_id), "w") as tmp_og:
                tmp_og.write(og[0])
                tmp_og.write(og[1])
            #run the R subprocess, which should print info about the tree to stdout
            rscript = subprocess.run(command, shell = True)
            #once r is finished, opening the output
            with open("{0}_from_r.csv".format(cur_id), "r") as r_file:
                master_list = []
                for row in r_file:
                    master_list.append(row)
                #append to a master variable
                master_tuple = (og_name, master_list)
        line_of_output = writing(master_tuple)

    except IOError:
        print("Issue reading file")


def writing(content):
    #r_info will be the master_tuple produced in the model function, and passed to this one.
    results_dict = {}
    group_num = ""
    global first_time
    write_mode = "w"

    if content == tuple():
        return
        #"group_num" is the OG element of the tuple, while "presabs" is the list element
    group_num = content[0]
    presabs = content[1]
    all_nodes = []
    #skipping the first row, which is just a 0 and a 1
    for item in presabs[1:]:
        #stripping off the linefeeds and splitting on tabs
        #also taking off the quotation marks from the node names
        #"first_line" is there to be written to a file later
        stripped_item = item.rstrip()
        fields = stripped_item.split("\t")
        stripped_fields = fields[0].strip('"')
        all_nodes.append(stripped_fields)
        #key = OG number, value = empty list, later presense scores
        results_dict.setdefault(group_num, [])
        results_dict[group_num].append(fields[2])
    with lock:
        write_mode = "w" if first_time.value == 0 else "a"
        try:
            with open("{0}".format(args.output), write_mode) as final:
                first_line = "\t".join(all_nodes)
                #check to see if it is the first time running through this function
                #if it is, write the first line of the file (with all the node numbers)
                #then change first_time to equal 1 so that it won't be written again.
                #also change the mode of writing so that it will overwrite the first time, and append otherwise
                if first_time.value == 0:
                    final.write("\t{0}\n".format(first_line))
                    first_time.value = 1

                #if it is not the first time, write a normal line of OG info to the file
                for og_num in results_dict:
                    all_scores = "\t".join(results_dict[og_num])
                    whole_line = "{0}\t{1}\n".format(og_num, all_scores)
                    final.write(whole_line)

        except IOError:
            print("Problem writing outfile")



#arguments for the whole thing
parser = argparse.ArgumentParser(description = "arguments for applying the dollo model")
parser.add_argument("-p", "--phylotree", required = True, help = "Path to a phylogenetic tree file")
parser.add_argument("-m", "--matrix", required = True, help = "Path to a presense/absense matrix")
parser.add_argument("-o", "--output", required = True, help = "Path to the output file")
parser.add_argument("-t", "--threads", type = int, required = True, help = "Number of threads to use")
args = parser.parse_args()

#copying the files I need into the working directory so that R can access them
working = os.getcwd()
shutil.copyfile(args.phylotree, "{0}/tree.new".format(working))
shutil.copyfile(args.matrix, "{0}/matrix.csv".format(working))

#setting up the global variables for the writing function
lock = Lock()
first_time = Value("i", 0)

#setting up the pooling and reading in the matrix file
pool = Pool(args.threads)
file = open("matrix.csv", "r")
all_lines = file.readlines()
file.close()
#extract out headers - save as variable
first = all_lines[0]
newfirst = first.split("\t")
woclust = newfirst.remove("#cluster_id")
taxa_line = "\t".join(newfirst)
header = "\t{0}\n".format(taxa_line)
headers = [header] * (len(all_lines)-1)
#The model will be given the header line (the species names), and a line of orthogroup information
for_pool = zip(headers, all_lines[1:])

#####################################
#Actual pool command - here is where r gets set off, and the file starts writing!!
pool.map(model, for_pool)

#cleaning up the temp files at the end
#scan through the working directory and look for a regex that matches the files to and from r
#if a match to these files is found, delete it
for entry in os.scandir(working):
    temps = re.search("\d+_from_r\.csv|\d+_for_r\.csv", entry.name)
    if temps:
        os.remove(entry.name)


#/mnt/lustre/macmaneslab/jlh1023/pipeline_dev/pipeline_scripts/dollo_model.py
#/mnt/lustre/plachetzki/shared/reciprocator/RECIPROCATOR/rax2/RAxML_bestTree.met_67_test
#/mnt/lustre/macmaneslab/jlh1023/metazoa_matrix/Results_Jul17/top_cor_pres_abs.csv
