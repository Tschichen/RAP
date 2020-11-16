# RAP
Ribozeq Analysis Pipeline
latest version: 0.1 (16.11.2020)

The bash scripts provided in this repository are used to evaluate the output of the [NextSnakes pipeline](https://github.com/jfallmann/NextSnakes). The necessary configurations for the evaluation of the Ribozeq data are explained in detail there. 

## Quantification of ribozyme annotation sites in species' genomes

To analyze annotation sites of ribozymes in a species, run the following script:

`sh cmsearch_analysis.sh PATHTOPEAKFILEDIRECTORY E-VALUETHRESHOLDFORHITS`

Count, length, and e-values of annotation sites under the given threshold are saved in several tab-separated csv files. Additionally, visualisations are given in the plots directory. 

## Quantification of ribozyme peaks from Ribozeq experiments

To analyze peaks representing ribozymes, run the following script:

`sh peak_analysis.sh PATHTODIRECTORYWITHPEAKFILES PATHTORIBOZYMEANNOTATION`

Count of ribozyme peaks are saved in several tab-separated csv files. Additionally, visualisations are given in the plots directory. 
