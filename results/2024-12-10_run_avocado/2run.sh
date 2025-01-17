#!/bin/bash
set -e -x

scratch="/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
data_dir="../../data/2024-12-04_encode_data"
#conda_env="avocado"

# Transform .big files to .wig files
function transform_to_wig {
  mkdir -p ${scratch}/transform_to_wig
  while read sample assay link; do
    # Get file name from $link
    fn=$(basename "$link")
	bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -R "rusage[mem=5000]" -o job.txt \
  		"python 2big_to_wig.py \
  		${data_dir}/${sample}/${assay}/${fn} \
  		${scratch}/transform_to_wig/4${sample}_${assay}.wig"
  done < ${data_dir}/url_links.txt
}

# Test with a specific sample and assay
function test {
  mkdir -p ${scratch}/test_avo

  # Set the specific file for testing
  sample="GM06690"
  assay="H3K27me3"
  input_file="${scratch}/transform_to_wig/4${sample}_${assay}.wig"
  output_file="${scratch}/test_avo/4${sample}_${assay}_test.wig"

  bsub -P acc_oscarlr -q gpu -n 1 -W 24:00 -o job.txt \
    "python single_avo.py \
        ${input_file} \
        ${output_file}"
}

# Running avocado analysis
function running_avocado {
  mkdir -p ${scratch}/avocado_analysis
  bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -o job.txt \
    "python avocado_analysis.py \
        ${scratch}/transform_to_wig/4${sample}_${assay}.wig \
        ${scratch}/avocado_analysis/4${sample}_${assay}.wig"
}

#transform_to_wig
test
# running_avocado

