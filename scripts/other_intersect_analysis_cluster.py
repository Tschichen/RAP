#/usr/bin/env python3
# other_intersect_analysis_cluster.py ---
#
# Filename: other_intersect_analysis_cluster.py 
# Contents: Analyse peaks from SCRibo-seq experiments that are not ribozymes
# Description:counts peaks from SCRibo-seq experiments that were intersected with the species genomes annotation. Additional, heights and widths of peaks, and their means and medians are calculated. For further plotting CSV files were generated.
# Author: Christiane Gaertner
# Version: 0.1
# Package-Requires: argparse, os, pathlib, numpy, pandas


# CODE

# IMPORTS
import argparse
import os
import pandas as pd
from pathlib import Path
import numpy as np

# returns path of input directory
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

# returns path of output directory
def dir_outpath(string):
    if os.path.isdir(string):
        return string
    else:
        this_dir = os.getcwd()
    dir_path = this_dir + "/" + string
    Path(dir_path).mkdir()
    return string

# count frequenz of peaks of different annotation types
def count_other(file, position):
    input = file.readlines()
    count_others = {}

    for line in input:
        line = str(line).split("\t")
        other = line[position]
        ribo = line[8]
        if ribo != "RiboCluster":
            if other in count_others.keys():
                count = count_others[other]
                count += 1
                count_others[other] = count
            else:
                count_others[other] = 1

    print(count_others)

    return count_others

# parse heights and lenghts of peaks of different annotation types
def quantify_other(file, position):
    input = file.readlines()
    cluster_others = {}

    for line in input:
        line = str(line).split("\t")
        other = line[position]
        length = abs(int(line[2])-int(line[1]))
        height = float(line[4])
        ribo = line[8]
        if ribo != "RiboCluster":
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

# calculate median and mean heights and lenghts of peaks of different annotation types
def find_mean_peak_height_to_length(cluster_others_quantify):
    mean_dict = {}
    for other in cluster_others_quantify.keys():
        other_name = str(other)
        other_arrays = cluster_others_quantify[other_name]
        length_array = other_arrays[0]
        height_array = other_arrays[1]
        means = []
        widths = []
        for i in range(len(height_array)):
            relative_value = float(height_array[i]) / float(length_array[i])
            widths.append(length_array[i])
            means.append(relative_value)
        value = np.mean(means)
        median = np.median(means)
        mean_length = np.mean(widths)
        median_length = np.median(widths)
        mean_dict[other_name] = [value, median, mean_length, median_length]

    return mean_dict

# MAIN
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
            mean_dict = find_mean_peak_height_to_length(other_cluster_dict)

            filename_means = out_dir + "/" + "other_peaks_mean" + input_name + ".csv"
            Path(filename_means).touch()
            with open(filename_means, "w") as out_file:
                header = "hit\tmean_height\tmedian_height\tmean_width\tmedian_width\n"
                out_file.write(header)
                for category in mean_dict.keys():
                    hit_name = str(category)
                    mean_median = mean_dict[hit_name]
                    mean = mean_median[0]
                    median = mean_median[1]
                    mean_length = mean_median[2]
                    median_length = mean_median[3]
                    new_line = hit_name + "\t" + str(mean) + "\t" + str(median) + "\t" + str(mean_length) + "\t" + str(median_length) + "\n"
                    out_file.write(new_line)
# other_intersect_analysis_cluster.py ends here