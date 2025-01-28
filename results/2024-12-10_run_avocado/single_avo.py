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

# Set paths
scratch =  sys.argv[1]
sample_name = "GM06690"
assays = ["H3K36me3", "H3K27me3"]
model_path = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data/avocado-chr14/avocado-chr14"

# Initialize data dictionary
data = {}

# Load data for each assay
for assay in assays:
    wig_filename = "%s/transform_to_wig/%s_%s.wig" % (scratch, sample_name, assay)  # .wig files instead of .npy
    values = read_wig_file(wig_filename)  # Read the .wig file
    data[(sample_name, assay)] = values  # Store positions and values

# Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Make a prediction for the H3K4me3 assay
track = model.predict(sample_name, "H3K4me3")

# Define output file path for the prediction
output_file = sys.argv[2]

# Write the predicted values to a WIG file
write_wig_file(track, output_file)

# Print the prediction results
print(f"Prediction for {sample_name} H3K4me3: {track}")
print(f"Predicted WIG file saved to: {output_file}")
