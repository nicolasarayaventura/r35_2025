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
  input_file="${scratch}/transform_to_wig/${sample}_${assay}.wig"
  output_file="${scratch}/test_avo/4${sample}_${assay}_test.wig"

  bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -R "rusage[mem=8000]" -o job.txt \
    "python single_avo.py \
        ${input_file} \
        ${output_file}"
}

# Running avocado analysis
function run_avo {
  # Define the samples array
  samples=("GM06690_H3K4me3" "GM23248_H3K36me3")

  rm -rf ${scratch}/avo_analysis
  mkdir -p ${scratch}/avo_analysis

  for sample in "${samples[@]}"; do
    assay=$(echo $sample | awk -F'_' '{print $2}')
    input_wig="${scratch}/transform_to_wig/${sample}_${assay}.wig"
    output_predictions="${scratch}/test_avo/4${sample}_test.txt"

    mkdir -p "${scratch}/test_avo"

	bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -R "rusage[mem=6000]" -o "${scratch}/avo_analysis/job_${sample}_run_avo.txt" \
 	 "python run_avo.py ${input_wig} ${output_predictions}"

  done
}
function test_plot {
  mkdir -p ${scratch}/test_avo
  plot_dir="${scratch}/plots"
  mkdir -p ${plot_dir}

  # Set the specific file for testing
  sample="GM06690"
  assay="H3K27me3"
  input_file="${scratch}/transform_to_wig/4${sample}_${assay}.wig"
  output_file="${scratch}/test_avo/4${sample}_${assay}_test.wig"

  bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -R "rusage[mem=6000]" -o job_plots.txt \
    "python single_plots_avo.py \
        ${input_file} \
        ${output_file} \
        --plot-dir ${plot_dir}"
}
function test_multi_plot {
  plot_dir="${scratch}/plots"
  mkdir -p ${plot_dir}

  # List of sample names and assays
  samples=("GM06690" "GM23248")
  assays=("H3K4me3" "H3K36me3" "H3K27me3")

  # Loop over each sample and assay to process
  for sample_name in "${samples[@]}"; do
    for assay in "${assays[@]}"; do
      # Set input and output file paths
      input_file="${scratch}/transform_to_wig/${sample_name}_${assay}.wig"
      output_file="${scratch}/test_avo/${sample_name}_${assay}_test.wig"
      output_plot_file="${plot_dir}/${sample_name}_${assay}_imputation.png"

      # Submit the job using bsub
      bsub -P acc_oscarlr -q premium -n 1 -W 24:00 -R "rusage[mem=6000]" -o job_${sample_name}_${assay}_multiplot.txt \
        "python multi_plot_avo.py \
          --input_file ${input_file} \
          --output_file ${output_file} \
          --plot-dir ${plot_dir} \
          --sample_name ${sample_name} \
          --assay ${assay} \
          --output_plot_file ${output_plot_file}"
    done
  done
}

#transform_to_wig
test_multi_plot
#test_plot
#test
#run_avo
