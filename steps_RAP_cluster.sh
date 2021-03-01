#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too, named peaks
# $1 = path to ribozyme annotation
anno_path=$1 # absolute path to .clstr file
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