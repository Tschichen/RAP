# SCALPEL (SCRibo-seq analysis pipeline)
latest version: 0.2 (12.04.2021)

The scripts provided in this repository can be used to manipulate data from SCRibo-Seq experiments using the [NextSnakes pipeline](https://github.com/jfallmann/NextSnakes). The necessary configurations to process the SCRibo-Seq data are explained in detail there. 

## Quantification of ribozyme annotation sites in species' genomes

After running cmsearch to find ribozyme annotation sites (included in the NextSnakes pipelines), *cmsearch* output files can be analyzed with *cmsearch_analysis.sh*. the script gives results for single ribozyme types. The bed files for each investigated CM should be copied or linked to one directory.

`sh cmsearch_analysis.sh PATHTORIBOBEDFILEDIRECTORY E-VALUETHRESHOLDFORHITS`

Count, length, and e-values of annotation sites under the given threshold are saved in several tab-separated csv files. Additionally, visualisations are provided in the cmsearch_plots directory. 

## Quantification of ribozyme peaks from Ribozeq experiments

To analyze peaks from SCRibo-seq experiments, link or copy peak files from peak finding to the directory "peaks".
Then run the following script:

`sh peak_analysis.sh PATHTORIBOZYMEANNOTATION`

`sh peak_analysis_other.sh PATHTORIBOZYMEANNOTATION PATHTOGENOMEANNOTATION`

Frequenz of either ribozyme or other peaks are saved in several tab-separated csv files. Additionally, visualisations are given in the plots directory. 
