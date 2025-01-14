import os
import glob
import subprocess
import numpy
from tensorflow import keras
from avocado import Avocado

wig_files = sys.argv[1]
avocado_analysis = sys.argv[2]

model = Avocado.load("avocado-chr14")
data = {}

assays = ["H3K36me3", "H3K27me3"]

scratch = "/sc/arion/scratch/arayan01/projects/r35_2025/results/2024-12-10_run_avocoda"
sample_name = "GM06690"

for assay in assays:
    filename = "%s/transform_to_wig/%s_%s" % (scratch, sample_name, assay)  # Use straight quotes here
    data[(sample_name, assay)] = numpy.load(filename)['arr_0']

model.fit_celltypes(data, n_epochs=5)

track = model.predict(sample_name, "H3K4me3")  # Use straight quotes here as well

