#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too, named peaks
# $1 = path to ribozyme annotation
anno_path=$1
mkdir intersect_ribo_anno
mkdir ribo_peaks_csv
mkdir plots
cd peaks
anno="../"
anno_dir=$anno$anno_path
for i in *; 
do
if [[ $i =~ "_peak_sorted" ]]
then
bedtools intersect -a $i -b $anno_dir -wa -wb -s > ../intersect_ribo_anno/${i}_intersect_ribo.bed
fi
done
cd ..
python3 scripts/Ribo_intersect_analysis_cluster.py -i intersect_ribo_anno -o ribo_peaks_csv -p
cd ribo_peaks_csv
for f in *
do
	name=${f##*/}
	string1="../plots/"
	string2="_peaks"
	plot_name=$string1$name$string2
	Rscript ../scripts/plot_ribo_peaks.R $f $name $plot_name
done