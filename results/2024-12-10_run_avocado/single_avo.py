import numpy as np
from avocado import Avocado

# Function to read WIG file
def read_wig_file(filename):
    positions = []
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('track') or line.startswith('browser'):
                continue
            parts = line.strip().split()
            if len(parts) == 2:
                positions.append(parts[0])
                values.append(parts[1])
    return positions, values

# Set paths
scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
sample_name = "GM06690"
assays = ["H3K36me3", "H3K27me3"]
model_path = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data/avocado-chr14/avocado-chr14"

# Initialize data dictionary
data = {}

# Load data for each assay
for assay in assays:
    wig_filename = "%s/transform_to_wig/%s_%s.wig" % (scratch, sample_name, assay)  # .wig files instead of .npy
    positions, values = read_wig_file(wig_filename)  # Read the .wig file
    data[(sample_name, assay)] = (positions, values)  # Store positions and values

# Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Make a prediction for the H3K4me3 assay
track = model.predict(sample_name, "H3K4me3")

# Print the prediction results
print(f"Prediction for {sample_name} H3K4me3: {track}")

