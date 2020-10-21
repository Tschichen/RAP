rule UMITOOLS_DEDUP:
    input: "MAPPED/{file}_mapped.sam"
    output: "MAPPED/{file}_mapped_dedup.sam"
    conda:  "snakes/envs/umi_tools.yaml"
    threads: 1
    shell:  "umi_tools dedup -I {input[0]} --output-stats=deduplicated --paired -S {output[0]}"