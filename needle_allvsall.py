# Conducts pairwise alignemnts of all protein seqeunces in a given fasta file using EMBOSS Needle and organizes the output in a similarity matrix

import os
import subprocess
from Bio import SeqIO
import numpy as np
import pandas as pd

fasta_file = 'all_nucleoside.fasta'
sequences = list(SeqIO.parse(fasta_file, 'fasta'))
sequence_ids = [seq.id for seq in sequences]

# Initialize the matrix
n = len(sequences)
alignment_matrix = np.zeros((n, n), dtype=int)

# Function to perform pairwise alignment using needle
def run_needle(seq1, seq2, output_file):
    cmd = [
        'needle',
        '-asequence', f'asis:{seq1}',
        '-bsequence', f'asis:{seq2}',
        '-gapopen', '10.0',
        '-gapextend', '0.5',
        '-outfile', output_file
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Error running needle for sequences:\n{seq1}\n{seq2}\n")
        print(result.stderr.decode())
        return None
    return output_file

# Loop through all sequences and perform pairwise alignments
for i in range(n):
    for j in range(i, n):
        output_file = f'temp_alignment_{i}_{j}.needle'
        output_file = run_needle(str(sequences[i].seq), str(sequences[j].seq), output_file)
        
        if output_file is None:
            continue

        # Parse the needle output file to get the alignment score
        with open(output_file, 'r') as f:
            found = False
            for line in f:
                if line.startswith('# Identity:'):
                    found = True
                    # Extract value between parentheses and discard decimals
                    print(f"Alignment result for {sequences[i].id} vs {sequences[j].id}: {line.strip()}")
                    score = line.split('(')[1].split('%')[0].split('.')[0]
                    alignment_matrix[i, j] = int(score)
                    alignment_matrix[j, i] = int(score)
                    break
            if not found:
                print(f"No identity score found for {sequences[i].id} vs {sequences[j].id}")

        os.remove(output_file)

# Converting the matrix to a pandas DataFrame for better visualization and saving it as a CSV file
alignment_df = pd.DataFrame(alignment_matrix, index=sequence_ids, columns=sequence_ids)
alignment_df.to_csv('alignment_scores_matrix.csv')
