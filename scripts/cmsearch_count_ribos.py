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
    

def length_calculation(input_file, threshold):
    length_dict = {}
    file = input_file.readlines()
    for line in file:
        line_array = line.strip().split("\t")
        ribo = line_array[3]
        if float(line_array[4]) <= threshold:
            if ribo in length_dict.keys():
                length_array = length_dict[ribo]
                length_array.append(abs(int(line_array[2]) - int(line_array[1])+1))
            else:
                length_array = [abs(int(line_array[2]) - int(line_array[1])+1)]
                length_dict[ribo] = length_array

    return length_dict
    
def eval_calculation(input_file, threshold):
    eval_dict = {}
    file = input_file.readlines()
    for line in file:
        line_array = line.strip().split("\t")
        ribo = line_array[3]
        if float(line_array[4]) <= threshold:
            if ribo in eval_dict.keys():
                eval_array = eval_dict[ribo]
                eval_array.append(float(line_array[4]))
            else:
                eval_array = [float(line_array[4])]
                eval_dict[ribo] = eval_array

    return eval_dict


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
    parser.add_argument('-c', '--count', action='store_true', help="If amount of ribozyme hits in cmsearch output should be counted")
    parser.add_argument('-l', '--length', action='store_true', help="If length of ribozyme hits in cmsearch output should be evaluated")
    parser.add_argument('-e', '--eval', action='store_true', help="If evalues of ribozyme hits in cmsearch output should be evaluated")
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

    if args.count:
        for file in cm_files:
            name = str(file).split("/")[-1][:-4]
            with open(file, "r") as input_file:
                ribo_dict = count_ribozymes(input_file, args.threshold)
                print(ribo_dict)
                s = pd.Series(ribo_dict, name = 'count')
                s.index.name = 'ribozyme'
                ribo_count_df = pd.DataFrame(s)
                filename = out_dir + "/" + name + "_count.csv"
                Path(filename).touch()
                ribo_count_df.to_csv(filename, sep="\t", header=True)

    if args.length:
        for file in cm_files:
            name = str(file).split("/")[-1][:-4]
            with open(file, "r") as input_file:
                ribo_dict_length = length_calculation(input_file, args.threshold)
                filename = out_dir + "/" + name + "_length.csv"
                with open (filename, "w+") as out_file:
                    out_file.write("ribozyme\tlength\n")
                    for key, value in ribo_dict_length.items():
                        for length in value:
                            s = str(key) + "\t" + str(length)
                            out_file.write(s)
                            out_file.write("\n")
    
    if args.eval:
        for file in cm_files:
            name = str(file).split("/")[-1][:-4]
            with open(file, "r") as input_file:
                ribo_dict_eval = eval_calculation(input_file, args.threshold)
                filename = out_dir + "/" + name + "_eval.csv"
                with open (filename, "w+") as out_file:
                    out_file.write("ribozyme\teval\n")
                    for key, value in ribo_dict_eval.items():
                        for eval in value:
                            s = str(key) + "\t" + str(eval)
                            out_file.write(s)
                            out_file.write("\n")