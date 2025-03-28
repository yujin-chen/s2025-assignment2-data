#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
import gzip
from warcio.archiveiterator import ArchiveIterator
from cs336_data.extract_text import extract_text_from_html_bytes
from cs336_data.common import KOA_SCRATCH_PATH  
WARC_FILE_PATH = KOA_SCRATCH_PATH / "subsampled_positive_urls.warc.gz"
OUTPUT_FILE = KOA_SCRATCH_PATH / "labeled_high_quality_test.txt"
NUM_SAMPLES = 11000
MIN_LENGTH = 50   

def extract_webpage_contents(warc_path, num_samples, min_length):

    collected_responses = []
    
    # Read the WARC file and collect response records sequentially
    with gzip.open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                raw_html = record.content_stream().read()  
                # HTML cleaning
                cleaned_text = extract_text_from_html_bytes(raw_html).strip()

                # Ensure text length meets the minimum length
                if len(cleaned_text) >= min_length:
                    collected_responses.append(cleaned_text)

                    # Stop when reach the required number of samples
                    if len(collected_responses) >= num_samples:
                        break

    # Apply labeling format
    labeled_samples = [f"__label__high {text}" for text in collected_responses]

    return labeled_samples

# Extract and label samples
labeled_data = extract_webpage_contents(WARC_FILE_PATH, NUM_SAMPLES, MIN_LENGTH)

# Save to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for line in labeled_data:
        f.write(line + "\n\n")  

print(f"Successfully saved {len(labeled_data)} labeled samples to {OUTPUT_FILE}")
