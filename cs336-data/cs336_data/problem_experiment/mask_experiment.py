#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[2]
sys.path.append(str(CURRENT_FILE))
import random
from warcio.archiveiterator import ArchiveIterator
from cs336_data.extract_text import extract_text_from_html_bytes
from cs336_data.mask_pii import mask_emails, mask_phone_numbers, mask_ip_addresses
from cs336_data.problem_experiment.common import KOA_SCRATCH_PATH, PROBLEM_EXPERIMENT_PATH

WARC_FILE_PATH = KOA_SCRATCH_PATH / "CC-MAIN-20180420081400-20180420101400-00118.warc.gz"
OUTPUT_FILE_PATH = PROBLEM_EXPERIMENT_PATH / "mask_experiment_result.txt"

def run_masking_experiment(warc_path, output_path, num_samples=20):
   
    extracted_texts = []

    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                raw_html = record.content_stream().read()
                extracted = extract_text_from_html_bytes(raw_html)
                if extracted.strip():
                    extracted_texts.append(extracted)

    samples = random.sample(extracted_texts, min(num_samples, len(extracted_texts)))

    with open(output_path, "w", encoding="utf-8") as f:
        for idx, text in enumerate(samples, 1):
            masked_email, count_email = mask_emails(text)
            masked_phone, count_phone = mask_phone_numbers(masked_email)
            masked_ip, count_ip = mask_ip_addresses(masked_phone)

            output = (
                f"Sample {idx}:\n"
                f"Original Text:\n{text}\n\n"
                f"Masked Text:\n{masked_ip}\n\n"
                f"Emails Masked: {count_email}, Phones Masked: {count_phone}, IPs Masked: {count_ip}\n"
                + "-" * 80 + "\n"
            )

            print(output)
            f.write(output)

    print(f"\nMasking experiment complete. Output saved to {output_path}")

if __name__ == "__main__":
    run_masking_experiment(WARC_FILE_PATH, OUTPUT_FILE_PATH)
