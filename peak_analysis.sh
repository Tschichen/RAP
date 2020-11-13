#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with peak_files should be linked to this directory, too. The directory must be named "peakfiles" 
# Ribo annotation must be linked into RAP directory
cd peakfiles
mkdir ../intersect_ribo_anno && mkdir ../ribo_peaks_csv
for i in *_peak_sorted.bed.gz; do bedtools intersect -a $i -b Schisto_new_05_merged.bed -wa -wb > ../intersect_ribo_anno/${i}_intersect_ribo.bed; done
cd ..
python3 scripts/Ribo_intersect_analysis.py -i intersect_ribo_anno -o ribo_peaks_csv