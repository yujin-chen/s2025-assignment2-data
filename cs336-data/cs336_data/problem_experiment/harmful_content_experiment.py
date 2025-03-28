#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[2]
sys.path.append(str(CURRENT_FILE))
import random
from cs336_data.extract_text import extract_text_from_html_bytes
from cs336_data.harmful_content import toxic_speech_classify, nsfw_classify
from warcio.archiveiterator import ArchiveIterator
from cs336_data.problem_experiment.common import KOA_SCRATCH_PATH, PROBLEM_EXPERIMENT_PATH


WARC_FILE_PATH = KOA_SCRATCH_PATH / "CC-MAIN-20180420081400-20180420101400-00118.warc.gz"
OUTPUT_FILE_PATH = PROBLEM_EXPERIMENT_PATH / "harmful_content_result.txt"

def process_warc_file(warc_path, output_path, num_samples=20, threshold=0.6):
    extracted_texts = []

    with open(warc_path, "rb") as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == "response":
                raw_html = record.content_stream().read()
                extracted_text = extract_text_from_html_bytes(raw_html)
                if extracted_text.strip():
                    extracted_texts.append(extracted_text)

    sampled_texts = random.sample(extracted_texts, min(num_samples, len(extracted_texts)))
    harmful_count = 0

    with open(output_path, "w", encoding="utf-8") as out:
        print("\n=== Harmful Content Detection ===\n", file=out)

        for i, text in enumerate(sampled_texts):
            nsfw_label, nsfw_score = nsfw_classify(text)
            toxic_label, toxic_score = toxic_speech_classify(text)

            is_harmful = (nsfw_label == "nsfw" and nsfw_score > threshold) or \
                         (toxic_label == "toxic" and toxic_score > threshold)

            if is_harmful:
                harmful_count += 1

            print(f"Sample {i+1}:", file=out)
            print(f"Original Text:\n{text}\n", file=out)
            print(f"NSFW Score: {nsfw_score:.2f}, Label: {nsfw_label.upper()}", file=out)
            print(f"Toxic Score: {toxic_score:.2f}, Label: {toxic_label.upper()}", file=out)
            print(f"Predicted Harmful: {is_harmful}, \n (To be evaluated) manually harmful: ", file=out)
            print("-" * 80, file=out)

        fraction_harmful = harmful_count / num_samples

        print("\n=== Evaluation Summary ===", file=out)
        print(f"Total Samples: {num_samples}", file=out)
        print(f"Harmful Documents: {harmful_count}", file=out)
        print(f"(To be filled) False Positives: ", file=out)
        print(f"(To be filled) False Negatives: ", file=out)
        print(f"Harmful Fraction: {fraction_harmful:.2f}", file=out)

if __name__ == "__main__":
    process_warc_file(WARC_FILE_PATH, OUTPUT_FILE_PATH)
    print(f"Report written to {OUTPUT_FILE_PATH}")
