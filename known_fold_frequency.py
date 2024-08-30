#Given a list of IDs (in this case the names of known effector families), it will calculate  the frequency of each in all 7 pathogens tested

from collections import defaultdict

with open('known_families.txt', 'r') as f:
    entries = [line.strip() for line in f]

# Define the prefixes to search for
prefixes = ['PBTT', 'spongo', 'albugo', 'synch', 'poly', 'taphrina_', 'UMAG']

# Initialize a dictionary to store the frequency of prefixes per entry
entry_prefix_count = {entry: defaultdict(int) for entry in entries}

with open('mcl_structure.out', 'r') as f:
    for line in f:
        for entry in entries:
            if entry in line:
                # Split the line into words
                words = line.split()
                # Count occurrences of words with the specified prefixes
                for word in words:
                    for prefix in prefixes:
                        if word.startswith(prefix):
                            entry_prefix_count[entry][prefix] += 1

# Print the header
header = ['Entry'] + prefixes
print(" ".join(header))

# Output the frequencies per entry
for entry, counts in entry_prefix_count.items():
    counts_str = " ".join(str(counts[prefix]) for prefix in prefixes)
    print(f'{entry} {counts_str}')
