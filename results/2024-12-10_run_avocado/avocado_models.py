#!/bin/env python
import sys
import os
import glob
from avocado import Avocado
from tensorflow import keras
# Load the model outside the loops (assuming it's the same for all samples)
model = Avocado.load("avocado-chr19")

samples = ["GM23248", "GM06690"]
assays = ["H3K3me1", "H3K3me37", "H3K3me2"]

scratch = "/tmp/data/2024-12-10_encode_data/"


def get_path(sample, assay):
    base_path = "%s/%s/%s" % (scratch, sample, assay)
    bigwig_files = glob.glob(os.path.join(base_path, "*.bigWig"))
    assert len(bigwig_files) == 1
    return bigwig_files[0]


for sample in samples:
    for assay in assays:
        data = {}

        # Load data for the current sample and assay
        data_path = get_path(sample, assay)
        data[(sample, assay)] = np.load(data_path)

        # Train the model with the loaded data
        model.fit_celltypes(data, n_epochs=5)

        # Define and use a variable for the output model path
        output_model = f"trained_model_{sample}_{assay}.h5"
        model.save(output_model)
