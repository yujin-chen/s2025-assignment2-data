#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[2]
sys.path.append(str(CURRENT_FILE))

from warcio.archiveiterator import ArchiveIterator
from cs336_data.extract_text import extract_text_from_html_bytes
from cs336_data.problem_experiment.common import KOA_SCRATCH_PATH, PROBLEM_EXPERIMENT_PATH


WARC_FILE_PATH = KOA_SCRATCH_PATH / "CC-MAIN-20180420081400-20180420101400-00118.warc.gz"  
OUTPUT_TEXT_FILE = PROBLEM_EXPERIMENT_PATH / "extracted_text.txt" 

def extract_text_from_warc(warc_file_path, output_path):
    
    with open(warc_file_path, 'rb') as warc_in, open(output_path, 'w', encoding='utf-8') as txt_out:
        for record in ArchiveIterator(warc_in):
            if record.rec_type == 'response':  # Process only HTTP responses (HTML content)
                raw_html = record.raw_stream.read()  # Read raw html
                
                try:
                    extracted_text = extract_text_from_html_bytes(raw_html) 
                    
                    if extracted_text:  # Ensure no empty response is extracted
                        txt_out.write(extracted_text)
                        txt_out.write("\n\n==== PAGE SEPARATOR ====\n\n")
                
                except Exception as e:
                    print(f"Error processing record: {e}") 

if __name__ == "__main__":
    extract_text_from_warc(WARC_FILE_PATH, OUTPUT_TEXT_FILE)
    print(f"Extraction complete. Saved to {OUTPUT_TEXT_FILE}")