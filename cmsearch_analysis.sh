#!/bin/sh
# should be executed in the RAP directory after cloning it. $1 directory with cmsearch output files: ribozyme_species.bed files, $2: e-value threshold for cmsearch hits
var1=$1;var2=$2
python3 scripts/cmsearch_count_ribos.py -i $var1 -o cmsearch_ribo_counts -t $var2 -c
python3 scripts/cmsearch_count_ribos.py -i $var1 -o cmsearch_ribo_lengths -t $var2 -l
python3 scripts/cmsearch_count_ribos.py -i $var1 -o cmsearch_ribo_evals -t $var2 -e
mkdir plots
FILES1=cmsearch_ribo_counts/*
for f in $FILES1
# TODO: convert f to string for length calculation!
do
	name=${f##*/}
	string1="plots/"
	string2="_count.pdf"
	plot_name = $string1$name$string2
	Rscript scripts/plot_cmsearch_count.R $f $name $plot_name
done
FILES2=cmsearch_ribo_lengths/*
for f in $FILES2
do
	name=${f##*/}
	string1="plots/"
	string2="_length.pdf"
	plot_name=$string1$name$string2
	Rscript scripts/plot_cmsearch_length.R $f $name $plot_name
done
FILES3=cmsearch_ribo_evals/*
for f in $FILES3
do
	name=${f##*/}
	string1="plots/"
	string2="_eval.pdf"
	plot_name=$string1$name$string2
	Rscript scripts/plot_cmsearch_eval.R $f $name $plot_name
done