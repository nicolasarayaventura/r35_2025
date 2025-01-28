import numpy as np
import os
import sys
from avocado import Avocado

# Function to read WIG file
def read_wig_file(filename):
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('track') or line.startswith('browser'):
                continue            
            parts = line.rstrip('\n').split('\t')
            value = float(parts[3])
            values.append(value)
    return values

# Function to write the predicted WIG file
def write_wig_file(prediction, filename, chrom="chr14", window_size=25):
    with open(filename, 'w') as f:
        # Add track line
        f.write("track type=wiggle_0\n")
        # Write the predicted values with positions
        for i, value in enumerate(prediction):
            start = i * window_size
            end = start + window_size
            f.write(f"{chrom}\t{start}\t{end}\t{value}\n")

def get_assays_to_add_to_model(assay_to_predict):
    all_assay = ["H3K36me3", "H3K27me3", "H3K4me3"]
    assays_to_add = []
    for assay in all_assay:
        if assay == assay_to_predict:
            continue
        assays_to_add.append(assay)
    return assays_to_add

# Set paths
#scratch =  sys.argv[1] # scratch directory
sample_name = sys.argv[1]
assay_to_predict = sys.argv[2] # H3K36me3
output_file = sys.argv[3]  # Define output file path for the prediction

assays = get_assays_to_add_to_model(assay_to_predict)

model_path = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data/avocado-chr14/avocado-chr14"

# Initialize data dictionary
data = {}

# Load data for each assay
for assay in assays:
    wig_filename = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda/transform_to_wig/%s_%s.wig" % (sample_name, assay)  # .wig files instead of .npy
    values = read_wig_file(wig_filename)  # Read the .wig file
    data[(sample_name, assay)] = values  # Store positions and values

# Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Make a prediction for the assay_to_predict assay
track = model.predict(sample_name, assay_to_predict)

# Write the predicted values to a WIG file
write_wig_file(track, output_file)

# Print the prediction results
print(f"Prediction for {sample_name} {assay_to_predict}: {track}")
print(f"Predicted WIG file saved to: {output_file}")
