import argparse
import os
import pandas as pd
from pathlib import Path


def dir_file(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


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


def parse_cluster_file(file):
    input = file.readlines()
    cluster_dict = {}
    for line in input:
        line = [x.strip() for x in str(line).split("\t")]
        cluster = line[0]
        count = line[1]
        cluster_dict[cluster] = count

    return cluster_dict


def calculate_count_to_height(file1, cluster_dict):
    count_to_height = {}
    input = file1.readlines()
    
    for line in input:
        line_array = [x.strip() for x in str(line).split("\t")]
        cluster = line_array[0]
        height = line_array[4]
        if float(height) > 1000:
            print(height)
            print(line_array)
        cluster_count = cluster_dict[cluster]
        if cluster in count_to_height.keys():
            scatter_array = count_to_height[cluster]
            scatter_array.append([cluster_count, height])
            count_to_height[cluster] = scatter_array
        else:
            count_to_height[cluster] = [[cluster_count, height]]
    #print(count_to_height)

    return count_to_height


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="analyse cluster and intersect files")
    parser.add_argument('-i', '--indir', type=dir_path, required=True, help="directory, where input files are stored")
    parser.add_argument('-o', '--outdir', type=dir_outpath, required=True, help="directory for output files")
    parser.add_argument('-c', '--cluster', type=dir_file, required=True, help="path were cluster info file is stored")
    args = parser.parse_args()

    file_dir = os.path.abspath(args.indir)

    out_dir = os.path.abspath(args.outdir)

    cluster_file = os.path.abspath(args.cluster)

    with open(cluster_file, "r") as handle3:
        cluster_dict = parse_cluster_file(handle3)

    intersect_files = []

    # r=root, d=directories, f = files
    for r, d, f in os.walk(file_dir):
        for file in f:
            intersect_files.append(os.path.join(r, file))

    for file in intersect_files:
        print(file)
        input_name = str(file).split("/")[-1]
        with open(file, "r") as handle:
            cluster_to_height = calculate_count_to_height(handle, cluster_dict)

            filename_count = out_dir + "/" + input_name + "_cluster_to_height.csv"
            Path(filename_count).touch()
            with open(filename_count, "w") as out_file:
                header = "cluster\treads\theight\n"
                out_file.write(header)
                for category in cluster_to_height.keys():
                    hit_name = str(category)
                    scatter_array = cluster_to_height[category]
                    for entry in scatter_array:
                        count = entry[0]
                        height = entry[1]
                        new_line = hit_name + "\t" + str(count) + "\t" + str(height) + "\n"
                        #print(new_line)
                        out_file.write(new_line)