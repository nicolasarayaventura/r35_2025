import numpy as np
import matplotlib.pyplot as plt
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

# Set paths
scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
sample_name = "GM06690"
assays = ["H3K36me3", "H3K27me3", "H3K4me3"]  # Include H3K4me3 assay
model_path = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data/avocado-chr14/avocado-chr14"

# Initialize data dictionary
data = {}

# Load data for each assay
for assay in assays:
    wig_filename = f"{scratch}/transform_to_wig/{sample_name}_{assay}.wig"
    values = read_wig_file(wig_filename)
    data[(sample_name, assay)] = values

# Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Load ground truth data for H3K4me3 assay
wig_filename_true = f"{scratch}/transform_to_wig/{sample_name}_H3K4me3.wig"
y_true = read_wig_file(wig_filename_true)

# Make predictions for the sample "GM06690" and the "H3K4me3" assay
y_hat = model.predict(sample_name, "H3K4me3")

# Define the genomic region for plotting
start, end = 12750, 15000
x = np.arange(start * 25 / 1000., end * 25 / 1000., 25 / 1000.)

# Compute MSE values
mse_global = ((y_hat - y_true) ** 2).mean()
baseline_mse = ((y_true - np.mean(y_true)) ** 2).mean()

# Plotting
plt.figure(figsize=(14, 4))

# Plot the Roadmap signal (y_true)
plt.subplot(211)
plt.title(f"How good is our GM06690 H3K4me3 Imputation? Global MSE: {mse_global:4.4}, Global Baseline MSE: {baseline_mse:4.4}", fontsize=16)
plt.fill_between(x, 0, y_true[start:end], color='b', label="Roadmap Signal (GM06690)")
plt.legend(fontsize=14)
plt.ylabel("Signal Value", fontsize=14)
plt.ylim(0, 7)  # Fixed y-limits for better visualization, adjust if necessary
plt.xlim(start * 25 / 1000., end * 25 / 1000.)

# Plot the Avocado imputation (y_hat)
plt.subplot(212)
plt.fill_between(x, 0, y_hat[start:end], color='g', label="Avocado Imputation")
plt.legend(fontsize=14)
plt.ylabel("Signal Value", fontsize=14)
plt.xlabel("Genomic Coordinate (kb)", fontsize=14)
plt.ylim(0, 7)  # Fixed y-limits, same as above
plt.xlim(start * 25 / 1000., end * 25 / 1000.)

# Show the plot
plt.show()

# Define the plot output path
output_plot_file = f"{scratch}/plots/{sample_name}_H3K4me3_imputation.png"
plt.savefig(output_plot_file, dpi=300, bbox_inches="tight")
