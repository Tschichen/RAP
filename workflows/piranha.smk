# INPUT for Piranha: (from Workflow peaks.smk) output from step: rule PreprocessPeaks needed!
# Probably it will be the best only to replace rule FindPeaks with Piranha rules
wildcard_constraints:
    type="sorted|unique"

rule Find_Peaks_Piranha:
    input:  "PEAKS/{file}_prepeak_{type}.bed.gz"
    output: "PEAKS/{file}_pir_peak_{type}.bed.gz"
    conda:  "snakes/envs/piranha.yaml"
    threads: 1
    shell:  "Piranha {input[0]} > {output[0]}"

rule Intersect_Peaks_Riboanno:
    input:  bed = "PEAKS/{file}_pir_peak_{type}.bed.gz",
            ann = "GENOMES/SPECIES_RIBO_ANNO_FILE.gff" # WO LIEGT DIE DANN?
    output: "PEAK_Intersect_Riboanno/{file}_intersect_piranha_riboanno_{type}.bed"
    conda:  "snakes/envs/bedtools.yaml"
    threads: 1
    shell:  "bedtools intersect -a {input.bed} -b {input.ann} -wa -wb > {output[0]}"

rule Quantify_Ribos:
    input:  directory = directory("PEAK_Intersect_Riboanno"),
            script = "scripts/count_short.py"
    output: directory("PEAK_Intersect_Riboanno_csv_files") # wird automatisch mit dem Python Script angelegt und geschrieben
    conda:  "snakes/envs/python.yaml"
    threads: 1
    shell:  "python3 {input.script} -i {input.directory} -o {output[0]}"

rule Find_Other_Hits:
    input:  bed = "PEAKS/{file}_pir_peak_{type}.bed.gz",
            ribos = "PEAK_Intersect_Riboanno/{file}_intersect_piranha_riboanno_{type}.bed"
    output: "PEAKS_without_ribos/{file}_pir_other_hits_{type}.bed.gz"
    conda:  "snakes/envs/bedtools.yaml"
    threads: 1
    shell:  "bedtools intersect -a {input.bed} -b {input.ribos} -v > {output[0]}"

rule Intersect_Other_Hits:
    input:  bed = "PEAK__without_ribos/{file}_pir_other_hits_{type}.bed.gz",
            ann = "GENOMES/SPECIES_OFF_ANNO_FILE.gff.gz"
    output: "PEAK_Intersect_off_anno/{file}_pir_other_hits_off_anno_{type}.bed.gz"
    conda:  "snakes/envs/bedtools.yaml"
    threads: 1
    shell:  "bedtools intersect -a {input.bed} -b {input.ribos} -wa -wb > {output[0]}"

rule Quantify_Other_Hits:
    input:  directory = directory("PEAK_Intersect_off_anno"),
            script = "scripts/analyse_bedtools_intersect_annotations.py"
    output: directory("PEAK_Intersect_off_anno_csv_files") # wird automatisch mit dem Python Script angelegt und geschrieben
    conda:  "snakes/envs/python.yaml"
    threads: 1
    shell:  "python3 {input.script} -i {input.directory} -o {output[0]}"