#!/bin/bash
set -e -x

scratch="/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
data_dir="../../data/2024-12-04_encode_data"
#conda_env="avocado"

# Test singular file first
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

test
