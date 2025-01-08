import os
import glob
import subprocess
from avocado import Avocado

# Ensure scratch is set
scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"  # Set scratch directory

# Function to parse files and extract sample/assay information
def get_sample_assay_files():
    wig_files = glob.glob(os.path.join(scratch, "*.wig"))
    sample_assay_map = {}
    for wig_file in wig_files:
        filename = os.path.basename(wig_file)
        if "_" in filename and filename.endswith(".wig"):
            sample, assay = filename.replace(".wig", "").split("_", 1)  # Splitting at the first underscore
            sample_assay_map[(sample, assay)] = wig_file
    return sample_assay_map

# Ensure output directory exists
output_dir = os.path.join(scratch, "avocado_analysis")
os.makedirs(output_dir, exist_ok=True)

# Get sample-assay map
sample_assay_files = get_sample_assay_files()

# Main processing loop
for (sample, assay), wig_file in sample_assay_files.items():
    try:
        print(f"Processing Sample: {sample}, Assay: {assay}, File: {wig_file}")

        # Define the output prediction file name
        output_predictions = os.path.join(output_dir, f"predictions_{sample}_{assay}.txt")

        # Build the Avocado CLI command for running the model
        cmd = [
            "avocado", "run",              # Use the 'run' command for predictions
            "--model", "avocado-chr19",    # Specify the pre-trained model
            "--input", wig_file,           # Input .wig file
            "--output", output_predictions # Output predictions file
        ]

        # Run the CLI command
        subprocess.run(cmd, check=True)

        print(f"Predictions saved to {output_predictions}")

    except subprocess.CalledProcessError as e:
        print(f"Subprocess error processing {sample}-{assay}: {e}")
    except Exception as e:
        print(f"Error processing {sample}-{assay}: {e}")
