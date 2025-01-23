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
            # line? "{chrom}\t{i*window_size}\t{i*window_size + window_size}\t{avg_value}\n"
            parts = line.rstrip('\n') # "{chrom}\t{i*window_size}\t{i*window_size + window_size}\t{avg_value}"
            parts = line.split('\t') # string to list, where every element is sandwiched between a \t
            value = float(parts[3])
            values.append(value)
    return values

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
    values = read_wig_file(wig_filename)  # Read the .wig file
    data[(sample_name, assay)] = values  # Store positions and values
   
 # Load the Avocado model
model = Avocado.load(model_path)

# Train the model on the loaded data
model.fit_celltypes(data, n_epochs=5)

# Make a prediction for the H3K4me3 assay
y_hat = model.predict(sample_name, "H3K4me3")  # Predictions

# Load y_true for H3K4me3 assay
wig_filename_true = "%s/transform_to_wig/%s_H3K4me3.wig" % (scratch, sample_name)
y_true = read_wig_file(wig_filename_true)  # Load ground truth from .wig file

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
    "How good is our E065 H3K4me3 Imputation? Global MSE: {:4.4}, Global Baseline MSE: {:4.4}".format(mse_global, baseline_mse),
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
output_plot_file = f"{scratch}/plots/{sample_name}_H3K4me3_imputation.png"
plt.savefig(output_plot_file, dpi=300, bbox_inches="tight")

