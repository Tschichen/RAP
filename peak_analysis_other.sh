#!/bin/sh
# This script should be executed in the SCALPEL directory after cloning it. 
# The peak files should be copied or linked to the peaks directory in this repository.
# $1 = absolute path to ribozyme or cluster annotation.
# $2 = absolute path to species genome annotation
ribo_anno_path=$1
genome_anno_path=$2
mkdir intersect_other_anno
mkdir no_intersection
mkdir plots
cd peaks
anno="../"
anno_dir=$anno$anno_path
for i in *; 
do
if [[ $i =~ "_peak_sorted" ]]
then
bedtools intersect -a $i -b $ribo_anno_path -v > ../no_intersection/${i}_no_intersect.bed
bedtools intersect -a ../no_intersection/${i}_no_intersect.bed -b $genome_anno_ath -wa -wb -s > ../intersect_other_anno/${i}_intersect_other.bed
fi
done
cd ..
python3 scripts/other_intersect_analysis.py -i intersect_other_anno -o other_peaks_csv -n
cd other_peaks_csv
for f in *
do
	name=${f##*/}
	string1="../plots/"
	string2="_other_peaks"
	plot_name=$string1$name$string2
	Rscript ../scripts/plot_other_peaks.R $f $name $plot_name
done