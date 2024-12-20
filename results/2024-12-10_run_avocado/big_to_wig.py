import os
import pyBigWig

work_data = "/sc/arion/work/arayan01/project/r35_2025/data/2024-12-04_encode_data"
scratch = "/sc/arion/scratch/arayan01/project/r35_2025/data/2024-12-04_encode_data/bigwig_towig"

def bigwig_to_wig(bw_file, output_file, chrom="chr14"):
    bw = pyBigWig.open(bw_file)
    with open(output_file, 'w') as wig:
        # Write the header for the Wig file
        wig.write("track type=wiggle_0\n")
        if chrom in bw.chroms():
            start = 0
            end = bw.chroms()[chrom]
            values = bw.values(chrom, start, end)
            
            # Write the data to the Wig file
            for i, value in enumerate(values):
                if value != float('nan'):  # Skip NaN values
                    wig.write(f"{chrom}\t{i}\t{i+1}\t{value}\n")
        else:
            print(f"Chromosome {chrom} not found in the BigWig file.")
    
    bw.close()

# Iterate over all BigWig files in the directory
for root, dirs, files in os.walk(work_data):
    for file in files:
        if file.endswith(".bigWig"):
            # Full path to the BigWig file
            bw_file = os.path.join(root, file)
            
            # Create the output file name by replacing .bigWig with .wig
            output_file = os.path.join(scratch, f"{os.path.basename(bw_file).replace('.bigWig', '.wig')}")
            
            # Convert the BigWig file to a Wig file for chrom "chr14"
            bigwig_to_wig(bw_file, output_file, chrom="chr14")
            
            print(f"Converted {bw_file} to {output_file}")
