import argparse
import os
from pathlib import Path
import numpy as np
import pandas as pd


def count_ribozymes(input_file, threshold):
	input_lines = input_file.readlines()
	ribo_dict = {}
	for line in input_lines:
		line_array = line.strip().split("\t")
		ribo = line_array[3]
		if float(line_array[4]) <= threshold:
			if ribo in ribo_dict.keys():
				count = ribo_dict[ribo]
				count += 1
				ribo_dict[ribo] = count
			else:
				ribo_dict[ribo] = 1
				
	return ribo_dict


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="calculation of statistics out of cmsearch results")
    parser.add_argument('-i', '--indir', type=dir_path, required=True, help="directory, where input files are stored")
    parser.add_argument('-o', '--outdir', type=dir_outpath, required=True, help="directory for output files")
    parser.add_argument('-t', '--threshold', type=float, default=10.0, help="enter upper threshold for e-value. "
                                                                            "Default = 10.0")
    args = parser.parse_args()

    file_dir = os.path.abspath(args.indir)

    out_dir = os.path.abspath(args.outdir)

    cm_files = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            cm_files.append(os.path.join(r, file))

    input_array = []

    print("The following files are examined: ")
    for file in cm_files:
        print(file)

    for file in cm_files:
        name = str(file).split("/")[-1][:-5]
        with open(file, "r") as input_file:
            ribo_dict = count_ribozymes(input_file, args.threshold)
            print(ribo_dict)
            s = pd.Series(ribo_dict, name = 'count')
            s.index.name = 'ribozyme'
            ribo_count_df = pd.DataFrame(s)
            filename = out_dir + "/" + name + "_count.csv"
            Path(filename).touch()
            ribo_count_df.to_csv(filename, sep="\t", header=True)