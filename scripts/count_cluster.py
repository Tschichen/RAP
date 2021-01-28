import argparse
import os
import pandas as pd
from pathlib import Path


def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def dir_outpath(string):
    if os.path.isdir(string):
        return string
    else:
        this_dir = os.getcwd()
    dir_path = this_dir + "/" + string
    Path(dir_path).mkdir()
    return string


def count_sequences_in_cluster(file):
    input = file.readlines()
    count_cluster = {}

    for line in input:
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analyse cluster files")
    parser.add_argument('-i', '--indir', type=dir_path, required=True, help="directory, where input files are stored")
    parser.add_argument('-o', '--outdir', type=dir_outpath, required=True, help="directory for output files")
    args = parser.parse_args()

    file_dir = os.path.abspath(args.indir)

    out_dir = os.path.abspath(args.outdir)

    cluster_files = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            bed_files.append(os.path.join(r, file))

    for file in cluster_files:
        print(file)
        input_name = str(file).split("/")[-1]
        with open(file, "r") as handle:
            
