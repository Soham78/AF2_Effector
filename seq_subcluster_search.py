#This code reads a list of member IDs from  a structure-based cluster and
# try to find which sequence based cluster have atleast one member from the structure ID list.



def find_matching_lines(values_file, tsv_file):
    # Read values from the first file
    with open(values_file, 'r') as file:
        values_set = {line.strip() for line in file}

    # read the TSV file
    matching_lines = []
    with open(tsv_file, 'r') as file:
        for line_index, line in enumerate(file, 1):
            # Split the line into values based on tab separation
            elements = line.strip().split('\t')
            # Check if any element in this line is in the set of values
            if any(element in values_set for element in elements):
                matching_lines.append(line_index)

    return matching_lines


values_file_path = 'structure_ids.txt'  # Path to the structure cluster IDs
tsv_file_path = 'sequence_mcl.tsv'       # Path to the sequence mcl output

matching_line_indices = find_matching_lines(values_file_path, tsv_file_path)

# Print the indices of matching lines
print("Lines containing at least one matching value:", matching_line_indices)
