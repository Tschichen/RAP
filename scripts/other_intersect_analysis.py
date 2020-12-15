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


def count_other(file, position):
    input = file.readlines()
    count_others = {}

    for line in input:
        line = str(line).split("\t")
        other = line[position]

        if other in count_others.keys():
            count = count_others[other]
            count += 1
            count_others[other] = count
        else:
            count_others[other] = 1

    print(count_others)

    return count_others


def quantify_other(file, position):
    input = file.readlines()
    cluster_others = {}

    for line in input:
        line = str(line).split("\t")
        other = line[position]
        length = abs(int(line[2])-int(line[1]))
        height = float(line[4])

        if other in cluster_others.keys():
            lengths_heights = cluster_others[other]
            lengths = lengths_heights[0]
            heights = lengths_heights[1]
            lengths.append(length)
            heights.append(height)
            cluster_others[other] = [lengths, heights]
        else:
            lengths = [length]
            heights = [height]
            cluster_others[other] = [lengths, heights]

    return cluster_others


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="count other in peaks in intersection with off. anno")
    parser.add_argument('-i', '--indir', type=dir_path, required=True, help="directory, where input files are stored")
    parser.add_argument('-o', '--outdir', type=dir_outpath, required=True, help="directory for output files")
    parser.add_argument('-n', '--notribo', action='store_true', help="if intersections with off. anno are tested")
    args = parser.parse_args()

    file_dir = os.path.abspath(args.indir)

    out_dir = os.path.abspath(args.outdir)

    bed_files = []

    if args.notribo:
        position = 9
    else:
        position = 10

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            bed_files.append(os.path.join(r, file))

    for file in bed_files:
        print(file)
        input_name = str(file).split("/")[-1][:-5]
        with open(file, "r") as handle:
            other_count_dict = count_other(handle, position)

            filename = out_dir + "/" + "others_peak_" + input_name + ".csv"

            with open(filename, "w") as out_file:
                header = "hit\tcount\n"
                out_file.write(header)
                for category in other_count_dict.keys():
                    hit_name = str(category)
                    if hit_name != "region":
                        count = str(other_count_dict[hit_name])
                        new_line = hit_name + "\t" + count + "\n"
                        out_file.write(new_line)

        with open(file, "r") as handle2:

            other_cluster_dict = quantify_other(handle2, position)

            filename_quanti = out_dir + "/" + "other_peaks_quantify_count" + input_name + ".csv"
            Path(filename_quanti).touch()
            with open(filename_quanti, "w") as out_file:
                header = "hit\tlength\theight\n"
                out_file.write(header)
                for category in other_cluster_dict.keys():
                    hit_name = str(category)
                    if hit_name != "region":
                        arrays = other_cluster_dict[hit_name]
                        length_array = arrays[0]
                        height_array = arrays[1]
                        for i in range(len(length_array)):
                            length = str(length_array[i])
                            height = str(height_array[i])
                            new_line = hit_name + "\t" + length + "\t" + height + "\n"
                            out_file.write(new_line)
