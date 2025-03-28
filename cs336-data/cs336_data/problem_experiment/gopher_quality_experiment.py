#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[2]
sys.path.append(str(CURRENT_FILE))
import gzip
import random
from warcio.archiveiterator import ArchiveIterator
from cs336_data.extract_text import extract_text_from_html_bytes 
from cs336_data.gopher_quality_filters import gopher_quality_filter  
from cs336_data.problem_experiment.common import KOA_SCRATCH_PATH, PROBLEM_EXPERIMENT_PATH

WARC_FILE_PATH = KOA_SCRATCH_PATH / "CC-MAIN-20180420081400-20180420101400-00118.warc.gz"
OUTPUT_FILE_PATH = PROBLEM_EXPERIMENT_PATH / "gopher_filter_result.txt"

def extract_text_from_warc(warc_file, num_samples=20):

    extracted_texts = []

    with gzip.open(warc_file, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                raw_html = record.content_stream().read()
                cleaned_text = extract_text_from_html_bytes(raw_html)  

                if cleaned_text and len(cleaned_text.split()) > 50:  # Ensure meaningful content
                    extracted_texts.append(cleaned_text)

    # Randomly sample up to num_samples texts
    return random.sample(extracted_texts, min(num_samples, len(extracted_texts)))

def evaluate_gopher_quality(warc_file):


    texts = extract_text_from_warc(warc_file, num_samples=20)

    results = []
    for text in texts:
        passes_filter = gopher_quality_filter(text)  
        results.append((text, passes_filter))

    return results

def save_gopher_evaluation(warc_path, output_file):
   
    results = evaluate_gopher_quality(warc_path)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Gopher Quality Filter Evaluation\n")
        f.write("="*50 + "\n\n")

        for idx, (text, decision) in enumerate(results, 1):
            f.write(f"Example {idx}:\n")
            f.write(text + "\n") 
            f.write(f"Filter Decision: {'Passed' if decision else 'Failed'}\n")
            f.write("Manual Decision: \n")
            f.write("-" * 80 + "\n")

    print(f"Evaluation saved to {output_file}")


if __name__ == "__main__":
    save_gopher_evaluation(WARC_FILE_PATH, OUTPUT_FILE_PATH)
