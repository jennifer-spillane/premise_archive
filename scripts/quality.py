#! /usr/bin/env python3

import shutil
import os
import subprocess
import argparse

def busco():
    #making sure there wont be any problems making directories
    shutil.rmtree("busco_out", ignore_errors = True)
    shutil.rmtree("above_thresh", ignore_errors = True)
    shutil.rmtree("below_thresh", ignore_errors = True)

    #storing the original location, making directories and changing locations
    orig_dir = os.getcwd()
    os.mkdir("busco_out")
    os.mkdir("above_thresh")
    os.mkdir("below_thresh")
    os.rename("config.ini", "busco_out/config.ini")
    os.chdir("busco_out")

    #looping through the files in a specified directory
    for entry in os.scandir("{0}".format(args.path)):
        print(entry.path)
        print(entry.name)
        #running busco with the metazoa database
        subprocess.run("run_BUSCO.py -i {0} -o {1}_qual -l {2}/metazoa_odb9 -m prot".format(entry.path, entry.name, orig_dir), shell = True)

        #opening the output files and finding the relevant score
        try:
            with open("run_{0}_qual/short_summary_{0}_qual.txt".format(entry.name)) as qual_file:
                score = 0
                count = 0
                for line in qual_file:
                    count += 1
                    line = line.rstrip()
                    if count == 8:
                        break
                print(line)
                score += float(line[3:7])
                print(score)
                #sorting the files based on the score
                if score < 50.0:
                    os.rename("{0}".format(entry.path), "{0}/below_thresh/{1}".format(orig_dir, entry.name))
                else:
                    os.rename("{0}".format(entry.path), "{0}/above_thresh/{1}".format(orig_dir, entry.name))
        except IOError:
            print("Issue reading file")

    #changing directories back to where we started
    os.chdir(orig_dir)
    os.rename("busco_out/config.ini", "{0}/config.ini".format(orig_dir))

parser = argparse.ArgumentParser(description = "Arguments for the final project pipeline")
parser.add_argument("path", help = "path to a directory containing protein datasets ready for busco")
args = parser.parse_args()

busco()
