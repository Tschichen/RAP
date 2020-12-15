#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too, named peaks
# $1 = path to official annotation
anno_path=$1
mkdir intersect_other_anno
mkdir other_peaks_csv
mkdir plots
cd peaks
anno="../"
anno_dir=$anno$anno_path
for i in *; 
do
if [[ $i =~ "_peak_sorted" ]]
then
bedtools intersect -a $i -b $anno_dir -wa -wb -s > ../intersect_other_anno/${i}_intersect_other.bed
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