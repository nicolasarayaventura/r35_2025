import numpy as np
import tensorflow as keras
from avocado import Avocado
import matplotlib.pyplot as plt

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

# Make predictions and plot for each sample-assay combination
for sample_name in samples:
    for assay in assays:
        # For the current assay, make predictions for its associated assays
        associated_assays = assays_to_predict.get(assay)
        
        if associated_assays:
            print(f"Making predictions for {sample_name} {assay} and its associated assays {associated_assays}")
            
            for associated_assay in associated_assays:
                # Make prediction for the associated assay
                y_hat = model.predict(sample_name, associated_assay)
                
                # Load ground truth for the associated assay
                wig_filename_true = f"{scratch}/transform_to_wig/{sample_name}_{associated_assay}.wig"
                y_true = read_wig_file(wig_filename_true)
                
                # Define start and end for plotting
                start, end = 12750, 15000
                x = np.arange(start * 25 / 1000., end * 25 / 1000., 25 / 1000.)
                
                # Compute MSE values
                mse_global = ((y_hat - y_true) ** 2).mean()
                baseline_mse = ((y_true - np.mean(y_true)) ** 2).mean()
                
                # Plotting
                plt.figure(figsize=(14, 4))
                plt.subplot(211)
                plt.title(
                    f"How good is our Imputation for {sample_name} {associated_assay}? Global MSE: {mse_global:.4f}, Global Baseline MSE: {baseline_mse:.4f}",
                    fontsize=16,
                )
                plt.fill_between(x, 0, y_true[start:end], color='b', label="Roadmap Signal")
                plt.legend(fontsize=14)
                plt.ylabel("Signal Value", fontsize=14)
                plt.ylim(0, 7)
                plt.xlim(start * 25 / 1000., end * 25 / 1000.)
                
                plt.subplot(212)
                plt.fill_between(x, 0, y_hat[start:end], color='g', label="Avocado Imputation")
                plt.legend(fontsize=14)
                plt.ylabel("Signal Value", fontsize=14)
                plt.xlabel("Genomic Coordinate (kb)", fontsize=14)
                plt.ylim(0, 7)
                plt.xlim(start * 25 / 1000., end * 25 / 1000.)
                
                # Define the plot output path
                output_plot_file = f"{scratch}/plots/{sample_name}_{associated_assay}_imputation.png"
                plt.savefig(output_plot_file, dpi=300, bbox_inches="tight")
                plt.close()
        else:
            print(f"No associated assays found for {sample_name} {assay}")
