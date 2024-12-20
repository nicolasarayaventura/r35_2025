#!/bin/bash
set -e -x


scratch=/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda
data_dir="../../data/2024-12-04_encode_data"


function transform_bigwig_files {
  mkdir -p ${scratch}/transform_bigwig_files
  cat ../../data/2024-12-04_encode_data/url_links.txt | while read sample assay link
  do
      # get file name from $link
      fn=`cat $link | rev | cut -f1 -d/ | rev`
      python bigwig_conversion.py \
          ../../data/2024-12-04_encode_data/${sample}/${assay}/${fn}
          ${scratch}/transform_bigwig_files/${sample}_${assay}.txt.gz
}

function running_avocado {
  python avodo_models.py

}

transform_bigwig_files
