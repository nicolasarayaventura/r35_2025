import os
import sys
import pyBigWig
import numpy as np
#averaged values displayed only
input_bigwig = sys.argv[1]
output_wig = sys.argv[2]

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
            for avg_value in averaged_values:
                 wig.write(f"{avg_value}\n")    
        else:
            print(f"Chromosome {chrom} not found in the BigWig file.")
    
    # Close the BigWig file
    bw.close()

bigwig_to_wig(input_bigwig,output_wig)



