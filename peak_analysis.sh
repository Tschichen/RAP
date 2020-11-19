#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too. 
# $1 = directory with files out of peak finding.
# $2 = path to ribozyme annotation
var1=$1;var2=$2
peak_dir=$var1
peak_files="/*"
peak_path=$peak_dir$peak_files
anno_path=$var2
mkdir intersect_ribo_anno && mkdir ribo_peaks_csv
for i in $peak_path
do
	name=${i##*/}
	bedtools intersect -a $i -b $anno_path -wa -wb > intersect_ribo_anno/${name}_intersect_ribo.bed
done
python3 scripts/Ribo_intersect_analysis.py -i intersect_ribo_anno -o ribo_peaks_csv
FILES=ribo_peaks_csv/*
for f in $FILES
do
	name=${f##*/}
	string1="plots/"
	string2="_peaks.pdf"
	plot_name=$string1$name$string2
	Rscript scripts/plot_ribo_peaks.R $f $name $plot_name
done