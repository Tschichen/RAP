#!/bin/sh
# should be executed in the RAP directory after cloning it. Directory with cmsearch output files (bed files that are built at the end of the cmsearch workflow) should be linked to this directory, too. The directory must be named "cmsearch_out"
python3 scripts/commandline_statistics.py -i cmsearch_out -o cmsearch_statistics_csv -t 0.05 -n ribos_cmsearch