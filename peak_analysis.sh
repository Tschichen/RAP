#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too. 
# $1 = directory with files out of peak finding.
# $2 = path to ribozyme annotation
var1=$1;var2=$2
cd $var1
anno="../"
anno_path=$anno$var2
mkdir ../intersect_ribo_anno && mkdir ../ribo_peaks_csv
for i in *_peak_*.bed.gz; do bedtools intersect -a $i -b $anno_path -wa -wb > ../intersect_ribo_anno/${i}_intersect_ribo.bed; done
cd ..
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