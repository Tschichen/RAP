#!/bin/sh
# This script should be executed in the SCALPEL directory after cloning it. 
# The peak files should be copied or linked to the peaks directory.
# $1 = absolute path to .clstr file
anno_path=$1 
mkdir intersect_cluster_anno
mkdir cluster_peaks_csv
mkdir plots_cluster
cd peaks
for i in *; 
do
if [[ $i =~ "_peak_sorted" ]]
then
bedtools intersect -a $i -b $anno_path -wa -wb > ../intersect_cluster_anno/${i}_intersect_cluster.bed
fi
done
cd ..
python3 scripts/Ribo_intersect_analysis_cluster.py -i intersect_cluster_anno -o cluster_peaks_csv
cd cluster_peaks_csv
for f in *
do
	name=${f##*/}
	string1="../plots/"
	string2="_peaks_cluster"
	plot_name=$string1$name$string2
	Rscript ../scripts/plot_ribo_peaks.R $f $name $plot_name
done