# SCALPEL (SCRibo-seq analysis pipeline)
latest version: 0.1 (16.11.2020)

The bash scripts provided in this repository can be used to evaluate the output of the [NextSnakes pipeline](https://github.com/jfallmann/NextSnakes). The necessary configurations to process the Ribozeq data are explained in detail there. 

## Quantification of ribozyme annotation sites in species' genomes

After running cmsearch to find ribozyme annotation sites (included in the NextSnakes pipelines), cmsearch output files can be analyzed with the following script. It points out results for single ribozyme types. 

`sh cmsearch_analysis.sh PATHTORIBOBEDFILEDIRECTORY E-VALUETHRESHOLDFORHITS`

Count, length, and e-values of annotation sites under the given threshold are saved in several tab-separated csv files. Additionally, visualisations are provided in the plots directory. 

## Quantification of ribozyme peaks from Ribozeq experiments

To analyze peaks representing ribozymes, link peak files from peak finding to the directory "peaks".
Then run the following script:

`sh peak_analysis.sh PATHTORIBOZYMEANNOTATION`

Counts of ribozyme peaks are saved in several tab-separated csv files. Additionally, visualisations are given in the plots directory. 
