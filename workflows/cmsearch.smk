rule CMSEARCH:
    input:  cm_file = "CMFILES/{file}.cm", # how to do for i in CMFILES do?
            genome = "GENOMES/SPECIES_GENOM.fa.gz",
    output: tbl="CMSEARCH/CMSEARCH_SPECIES_{file}.tbl",
            out="CMSEARCH/CMSEARCH_GENOMENAME_{file}"
    conda:  "snakes/envs/infernal.yaml"
    threads: 1
    params:  cpu=8,
    shell:  "cmsearch --cpu={params.cpu} --tblout={output.tbl} {input.cm_file} {input.genome} > {output.out}"

rule FURTHER_processing_1:
    input:  "CMSEATCH/CMSEARCH_GENOMENAME_{file}"
    output: "CMSEARCH/CMSEARCH_GENOMENAME_{file}.tab"
    threads: 1
    shell:  "sed 's/ \+/\t/g' {input[0]} > {output[0]}"

rule FURTHER_processing_2:
    input:  "CMSEARCH/CMSEARCH_GENOMENAME_{file}.tab"
    output: "CMSEARCH/CMSEARCH_SPECIES_{file}.bed"
    conda:  "snakes/envs/perl.yaml" # ???
    threads: 1
    shell:  "perl -wlane 'next if ($_ =~/#/); $strand = $F[9]; $start = ($strand eq "+") ? $F[7]-1 : $F[8]-1; $end = ($strand eq "+") ? $F[8] : $F[7]; print join("\t",$F[0],$start,$end,$F[2],$F[15],$strand,$F[3])' {input[0]} > {output[0]}"

rule FURTHER_processing_3:
    input:  "CMSEARCH/CMSEARCH_SPECIES_{file}.bed"
    output: "CMSEARCH/RIBOZYMES_CMSEARCH_GENOMENAME.bed"
    threads: 1
    shell:  "cat {input[0]}|sort -k1,1 -k2,2n |uniq > {output[0]}"

rule FURTHER_processing_4:
    input:  "CMSEARCH/RIBOZYMES_CMSEARCH_GENOMENAME.bed"
    output: "CMSEARCH/Ribo_minimal_GENOMENAME.bed"
    conda:  "snakes/envs/perl.yaml"
    threads: 1
    shell:  "cut -f1-7 {input[0]}|perl -wlane '$F[4]*=100;print join("\t",@F[0..3],int($F[4]),@F[5..6])' > {output[0]}"
