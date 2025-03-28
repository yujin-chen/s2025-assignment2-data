import os
from collections import defaultdict

def exact_line_deduplication(input_files, output_dir):
    line_counts = defaultdict(int)

    # Count occurrences of each line using hash
    for file_path in input_files:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line_hash = hash(line.strip())
                line_counts[line_hash] += 1

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write only unique lines to output files
    for file_path in input_files:
        output_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(file_path, "r", encoding="utf-8") as f, open(output_path, "w", encoding="utf-8") as out_f:
            for line in f:
                line_hash = hash(line.strip())
                if line_counts[line_hash] == 1:
                    out_f.write(line)
