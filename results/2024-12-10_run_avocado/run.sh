#!/bin/bash
set -e -x


scratch=/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda
data_dir="../../data/2024-12-04_encode_data"
conda_env="avocado"

function transform_to_wig {
  mkdir -p ${scratch}/transform_to_wig
  cat ../../data/2024-12-04_encode_data/url_links.txt | while read sample assay link
  do
      # get file name from $link
      fn=`cat $link | rev | cut -f1 -d/ | rev`
      bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -o job.txt \
          "python big_to_wig.py \
          ../../data/2024-12-04_encode_data/${sample}/${assay}/${fn}
          ${scratch}/transform_to_wig/${sample}_${assay}.wig"
}

function running_avocado {
  source activate $conda_env
  python avodo_analysis.py
  mkdir -p ${scratch}/avocado_analysis
  do
    bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -o job.txt \
        "python avocado_analysis.py \
        ../../data/2024-12-04_encode_data/${sample}/${assay}/${fn} \
        ${scratch}/avocado_analysis/${sample}_${assay}.wig"

}

transform_to_wig
