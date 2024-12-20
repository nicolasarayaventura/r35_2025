import os
import sys
import pyBigWig
import numpy as np

input_bigwig = sys.argv[1]
output_wig = sys.argv[2]

# Define the paths for the input directory and the output directory
#work_data = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data"
#scratch = "/sc/arion/scratch/arayan01/project/r35_2025/data/2024-12-04_encode_data/bigwig_towig"

# Ensure the scratch directory exists
#os.makedirs(scratch, exist_ok=True)

def bigwig_to_wig(bw_file, output_file, chrom="chr14", window_size=25):
    # Open the BigWig file
    bw = pyBigWig.open(bw_file)
    
    with open(output_file, 'w') as wig:
        # Write the header for the Wig file
        wig.write("track type=wiggle_0\n")
        
        # Check if the chrom exists in the BigWig file
        if chrom in bw.chroms():
            start = 0
            end = bw.chroms()[chrom]  # Get the length of the chromosome
            values = bw.values(chrom, start, end)
            
            # Replace NaN values with 0
            values = [0 if v != v else v for v in values]  # Replace NaN with 0
            
            # Compute the average of every 25 values
            averaged_values = [
                np.mean(values[i:i + window_size]) for i in range(0, len(values), window_size)
            ]
            
            # Write the averaged values to the Wig file
            for i, avg_value in enumerate(averaged_values):
                wig.write(f"{chrom}\t{i*window_size}\t{i*window_size + window_size}\t{avg_value}\n")
                
        else:
            print(f"Chromosome {chrom} not found in the BigWig file.")
    
    # Close the BigWig file
    bw.close()

bigwig_to_wig(input_bigwig,output_wig)

'''
# Iterate over all BigWig files in the directory and subdirectories
for root, dirs, files in os.walk(work_data):
    for file in files:
        if file.endswith(".bigWig"):
            # Full path to the BigWig file
            bw_file = os.path.join(root, file)
            
            # Replicate the directory structure in scratch
            relative_path = os.path.relpath(root, work_data)  # Get relative path of the current folder
            output_dir = os.path.join(scratch, relative_path)  # Create corresponding output directory in scratch
            os.makedirs(output_dir, exist_ok=True)
            
            # Create the output file name by replacing .bigWig with _averaged.wig
            output_file = os.path.join(output_dir, f"{os.path.basename(bw_file).replace('.bigWig', '_averaged.wig')}")
            
            # Convert the BigWig file to a Wig file for chrom "chr14" and compute averages
            bigwig_to_wig(bw_file, output_file, chrom="chr14")
            
            print(f"Converted {bw_file} to {output_file}")
'''


