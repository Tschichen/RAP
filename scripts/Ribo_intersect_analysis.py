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

    print(count_ribos)

    return count_ribos


def quantify_ribo(file):
    input = file.readlines()
    cluster_ribos = {}

    for line in input:
        line = str(line).split("\t")
        ribo = line[10]
        length = abs(int(line[2])-int(line[1]))
        height = float(line[4])

        if ribo in cluster_ribos.keys():
            lengths_heights = cluster_ribos[ribo]
            lengths = lengths_heights[0]
            heights = lengths_heights[1]
            lengths.append(length)
            heights.append(height)
            cluster_ribos[ribo] = [lengths, heights]
        else:
            lengths = [length]
            heights = [height]
            cluster_ribos[ribo] = [lengths, heights]

    print(cluster_ribos)

    return cluster_ribos


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

            ribo_count_df = pd.DataFrame.from_records([ribo_count_dict])

            filename = out_dir + "/" + "ribos_peak_" + input_name + ".csv"

            ribo_count_df.to_csv(filename, sep="\t", header=True)

        with open(file, "r") as handle2:

            ribo_cluster_dict = quantify_ribo(handle2)

            filename_quanti = out_dir + "/" + "ribo_peaks_quantify_count" + input_name + ".csv"
            Path(filename_quanti).touch()
            with open(filename_quanti, "w") as out_file:
                header = "hit\tlength\theight\n"
                out_file.write(header)
                for category in ribo_cluster_dict.keys():
                    hit_name = str(category)
                    arrays = ribo_cluster_dict[hit_name]
                    length_array = arrays[0]
                    height_array = arrays[1]
                    for i in range(len(length_array)):
                        length = str(length_array[i])
                        height = str(height_array[i])
                        new_line = hit_name + "\t" + length + "\t" + height + "\n"
                        out_file.write(new_line)