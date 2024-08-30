#Exctracts the pLDDT score of the highest rankind pdb file after an AlphaFold2 run

import os
import re

dir_path = "/Users/edelab/json_files"  
output_file = "/Users/edelab/json_files/output.txt"  

with open(output_file, 'w') as out:
    # loop over all files in the directory
    for filename in os.listdir(dir_path):
        if filename.endswith(".json"):  
            with open(os.path.join(dir_path, filename), 'r') as f:
                lines = f.readlines()[2:7]  
                max_value = max([float(re.search('[0-9]+\.?[0-9]*', line.split(":")[1]).group()) for line in lines])
                out.write(f"{os.path.splitext(filename)[0]}\t{max_value}\n")
