#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
from cs336_data.common import KOA_SCRATCH_PATH

# To put entire response into one line. So it can be use by fasttext
def format_labeled_data(input_file, output_file, max_samples=30000):

    formatted_lines = []
    sample_count = 0

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_label = None
    current_response = []

    for line in lines:
        line = line.strip()

        # Detect label 
        if line.startswith("__label__low") or line.startswith("__label__high"):
            # If there's an existing response, join it and save
            if current_label is not None:
                formatted_lines.append(f"{current_label} {' '.join(current_response) if current_response else ''}")
                sample_count += 1

                # Stop if reached the required number of samples
                if sample_count >= max_samples:
                    break

            current_label = line
            current_response = []
        else:
            # Append text to the current response 
            current_response.append(line)

    # Save the last response while keeping count
    if sample_count < max_samples and current_label is not None:
        formatted_lines.append(f"{current_label} {' '.join(current_response) if current_response else ''}")
        sample_count += 1

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(formatted_lines) + "\n")

    print(f"Successfully formatted and saved {sample_count} samples to {output_file}")

# Usage Example
INPUT_FILE = KOA_SCRATCH_PATH / "labeled_low_quality_test.txt"  
OUTPUT_FILE = KOA_SCRATCH_PATH / "formatted_labeled_low_quality_test.txt"

format_labeled_data(INPUT_FILE, OUTPUT_FILE, max_samples=30000)
