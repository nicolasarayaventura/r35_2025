import numpy as np
import tensorflow as keras
from avocado import Avocado

# Function to read WIG file
def read_wig_file(filename):
    values = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith('track') or line.startswith('browser'):
                continue
            parts = line.rstrip('\n').split('\t')  # string to list, where every element is sandwiched between a \t
            value = float(parts[3])  # Get the value (usually in the 4th column)
            values.append(value)
    return values

# Set paths
scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
samples = ["GM06690", "GM23248"]  # List of sample names
assays = ["H3K4me3", "H3K36me3", "H3K27me3"]  # List of assays
model_path = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data/avocado-chr14/avocado-chr14"

# Define assay mapping for predictions
assays_to_predict = {
    "H3K4me3": ["H3K36me3", "H3K27me3"],
    "H3K36me3": ["H3K4me3", "H3K27me3"],
    "H3K27me3": ["H3K36me3", "H3K4me3"]
}

# Initialize data dictionary
data = {}

# Load data for each sample-assay combination
for sample_name in samples:
    for assay in assays:
        wig_filename = f"{scratch}/transform_to_wig/{sample_name}_{assay}.wig"  # .wig files for each sample-assay
        values = read_wig_file(wig_filename)  # Read the .wig file
        data[(sample_name, assay)] = values  # Store the values for the assay

# Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Make predictions for each sample-assay combination based on the assay-to-assay mapping
for sample_name in samples:
    for assay in assays:
        # For the current assay, make predictions for its associated assays
        associated_assays = assays_to_predict.get(assay)
        
        if associated_assays:
            print(f"Making predictions for {sample_name} {assay} and its associated assays {associated_assays}")
            for associated_assay in associated_assays:
                # Predict for the associated assay
                track = model.predict(sample_name, associated_assay)
                print(f"Prediction for {sample_name} {associated_assay}: {track}")
        else:
            print(f"No associated assays found for {sample_name} {assay}")

