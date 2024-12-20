import os
import pyBigWig  
import numpy as np

data_dir = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data"
scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/data/2024-12-10_run_avocoda"

# numpy arcsinh function
def arcsinh_transform(data):
    return np.arcsinh(data)

# Function to process each BigWig file
def process_bigwig_file(bw_file, output_dir):
    bw = pyBigWig.open(bw_file)
    for chrom in bw.chroms():
        start = 0
        end = bw.chroms()[chrom]  # Get the length of the chromosome
        data = np.array(bw.values(chrom, start, end))
        
        # Apply arcsinh transformation
        transformed_data = arcsinh_transform(data)
        
        # Create output file name
        output_file = os.path.join(output_dir, f"{os.path.basename(bw_file)}_{chrom}.arcsinh.npz")
        
        # Save transformed data to npz format
        np.savez_compressed(output_file, data=transformed_data)
    
    bw.close()

# Function to process all BigWig files in the data directory
def process_all_files(data_dir, scratch):
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if file.endswith(".bigWig"):
                bw_file = os.path.join(root, file)
                
                # Process and save the transformed data
                process_bigwig_file(bw_file, scratch)

# Run the processing
process_all_files(data_dir, scratch)
