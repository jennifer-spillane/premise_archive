#! /usr/bin/env python3

#A program to run datasets through busco, then filter them with cdhit,
#and then run them through busco again

import argparse
import subprocess
import os

def qual_cdhit_qual():
    #recording the original directory and changing to one where the busco files will go
    orig_dir = os.getcwd()
    os.chdir("{0}".format(args.new_busco))
    #running busco a file that has gone through filter_transrate.py, before it is filtered again.
    busco1 = ("run_BUSCO.py -m tran -l /mnt/lustre/hcgs/shared/databases/busco/eukaryota_odb9 -i {0} -o {1}_trans".format(args.infile, args.prefix))
    subprocess.run(busco1, shell = True)

    #running cdhit on a file that has previously been filtered using filter_transrate.py
    print("Running cdhit")
    subprocess.run("cd-hit -c {0} -T 24 -i {1} -o {2}".format(args.similarity, args.infile, args.outfile), shell = True)

    os.chdir("{0}".format(args.final_busco))
    #running busco once more on the filtered (now twice) files
    busco2 = ("run_BUSCO.py -m tran -l /mnt/lustre/hcgs/shared/databases/busco/eukaryota_odb9 -i {0} -o {1}_cdhit".format(args.outfile, args.prefix))
    subprocess.run(busco2, shell = True)


parser = argparse.ArgumentParser(description = "Arguments for quality checking and filtering with cdhit")
parser.add_argument("-i", "--infile", required = True, help = "absolute path to file to be filtered and buscoed")
parser.add_argument("-s", "--similarity", type = float, default = 1.0, help = "similarity threshold for cdhit")
parser.add_argument("-n", "--new_busco", required = True, help = "path to directory where busco scores should be stored")
parser.add_argument("-f", "--final_busco", required = True, help = "path to directory where busco scores should be stored")
parser.add_argument("-b", "--orig_busco", required = True, help = "path to the directory where original busco score is")
parser.add_argument("-p", "--prefix", required = True, help = "prefix to go into the name of the busco output")
parser.add_argument("-o", "--outfile", required = True, help = "path to the filtered assembly file")
args = parser.parse_args()

qual_cdhit_qual()
