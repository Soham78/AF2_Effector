#Parallel execution of multiple TMalign runs using the specified number of cores and extraction of normalized TMScore for each pair.

import os
import glob
import re
import subprocess
import csv
from concurrent.futures import ProcessPoolExecutor

pdb_dir = './all_pdb'

# Get a list of all PDB files in the directory
pdb_files = glob.glob(os.path.join(pdb_dir, '*.pdb'))

# Output CSV file
output_file = './strcuture_clus_raw.csv'

# Function to run TM-align on a pair of PDB files
def run_tmalign(pair):
    pdb1, pdb2 = pair
    try:
        output = subprocess.check_output(['TMalign', pdb1, pdb2, '-a', 'T']).decode()
    except Exception as e:
        print(f"Failed to run TM-align on {pdb1} and {pdb2}: {e}")
        return pdb1, pdb2, 'Error'

    tm_score = 'N/A'
    for line in output.split("\n"):
        if 'if normalized by average length' in line:
            match = re.search(r'(0\.\d+|1\.0+)', line)
            if match:
                tm_score = match.group()
                break

    # Extracting only the file name, without the extension
    pdb1 = os.path.splitext(os.path.basename(pdb1))[0]
    pdb2 = os.path.splitext(os.path.basename(pdb2))[0]

    return pdb1, pdb2, tm_score

# Prepare a list of all pairs of PDB files
pairs = [(pdb1, pdb2) for i, pdb1 in enumerate(pdb_files) for pdb2 in pdb_files[i+1:]]

# Create a ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=100) as executor:  # max_worker determines number of cores to be  used
    # Run TM-align on all pairs of PDB files
    results = list(executor.map(run_tmalign, pairs))

# Write the results to the CSV file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['PDB1', 'PDB2', 'TM-score'])
    writer.writerows(results)
