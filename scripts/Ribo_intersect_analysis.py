import argparse
import pandas as pd
import os
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

def count_ribo(file):
    input = file.readlines()
    count_ribos = {}

    for line in input:
        line = str(line).split("\t")
        ribo = line[10]

        if ribo in count_ribos.keys():
            count = count_ribos[ribo]
            count += 1
            count_ribos[ribo] = count
        else:
            count_ribos[ribo] = 1
    new_names_dict = {}
    for entry in count_ribos.keys():
        if "Hammer" in str(entry) or "hammer" in str(entry):
            ribos = str(entry).split("|")
            new_key = ""
            for ribo in ribos:
                ribo_new = ribo.replace("Hammerhead", "HH")
                ribo_new = ribo_new.replace("hammerhead", "HH")
                new_key += ribo_new
                new_key += " "
            new_names_dict[new_key] = count_ribos[entry]
        else:
            new_names_dict[entry] = count_ribos[entry]
    
    print(new_names_dict)
    
    return new_names_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="count ribos in annotationsgit ")
    parser.add_argument('-i', '--indir', type=dir_path, required=True, help="directory, where input files are stored")
    parser.add_argument('-o', '--outdir', type=dir_outpath, required=True, help="directory for output files")
    args = parser.parse_args()

    file_dir = os.path.abspath(args.indir)

    out_dir = os.path.abspath(args.outdir)

    bed_files = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            bed_files.append(os.path.join(r, file))

    for file in bed_files:
        print(file)
        input_name = str(file).split("/")[-1][:-5]
        with open(file, "r") as handle:
            ribo_count_dict = count_ribo(handle)
            s = pd.Series(ribo_count_dict, name = 'count')
            s.index.name = 'ribozyme'
            ribo_count_df = pd.DataFrame(s)
            filename = out_dir + "/" + "ribo_peaks" + input_name + ".csv"
            Path(filename).touch()
            ribo_count_df.to_csv(filename, sep="\t", header=True)
