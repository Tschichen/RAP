EXTRACT

rule UMITOOLS_EXTRACT:
    input:  read1 = "FASTQ/{file}_r1.fastq.gz",
            read2 = "FASTQ/{file}_r2.fastq.gz"
    output: read1out = "FASTQ_UMI/{file}_r1_umi_extract.fq.gz"
            read2out = "FASTQ_UMI/{file}_r2_umi_extract.fq.gz"
    conda:  "snakes/envs/umi_tools.yaml"
    threads: 1
    params:  bc-pattern="NNNNNNNNTGGAATTCTCGGGTGCCAAGG"
    shell:  "umi_tools extract --stdin={input.read1} --bc-pattern={params.bc-pattern} --stdout={output.read1out} --read2-in={input.read2} --read2-out={output.read2out}"

# CAVE -> for mapping rules take files from FASTQ_UMI directory!