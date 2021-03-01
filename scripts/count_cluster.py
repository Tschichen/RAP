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

    blubb = 0
    for line in input:
        line = str(line).strip()
        if line.startswith(">"):
            if blubb > 0:
                count_cluster[cluster] = counter
            counter = 0
            cluster = line[1:]
            blubb += 1
        else:
            counter += 1
            
    print(count_cluster)

    return count_cluster

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
            cluster_files.append(os.path.join(r, file))

    for file in cluster_files:
        print(file)
        input_name = str(file).split("/")[-1]
        with open(file, "r") as handle:
            cluster_count = count_sequences_in_cluster(handle)

            filename_count = out_dir + "/" + "cluster_count.csv"
            Path(filename_count).touch()
            with open(filename_count, "w") as out_file:
                header = "cluster\tcount\n"
                out_file.write(header)
                for category in cluster_count.keys():
                    hit_name = str(category)
                    count = cluster_count[hit_name]
                    new_line = hit_name + "\t" + str(count) + "\n"
                    out_file.write(new_line)