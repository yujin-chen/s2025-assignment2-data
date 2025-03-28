#!/usr/bin/env python3
import sys
import os
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
import fasttext
from cs336_data.common import CS336_DATA_PATH
QUALITY_MODEL_PATH = CS336_DATA_PATH / "quality_classifier.bin"
QUALITY_MODEL_URL = "https://huggingface.co/yujin31/quality_classifier/resolve/main/quality_classifier.bin" 

# Ensure model exists or download it
def ensure_model(path: Path, url: str):
    if not path.exists():
        print(f"Quality classifier model not found at {path}, downloading from {url}...")
        os.system(f"wget -O {path} {url}")


ensure_model(QUALITY_MODEL_PATH, QUALITY_MODEL_URL)

# Load the model
quality_model = fasttext.load_model(str(QUALITY_MODEL_PATH))

def classify_quality(text: str):
    cleaned_text = " ".join(text.strip().split("\n"))

    if not cleaned_text:
        return "unknown", 0.0

    labels, scores = quality_model.predict(cleaned_text, k=1)
    detected_label = "high-quality" if labels[0] == "__label__high" else "low-quality"
    confidence_score = round(float(scores[0]), 4)

    return detected_label, confidence_score
