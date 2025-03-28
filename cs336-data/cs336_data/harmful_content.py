#!/usr/bin/env python3
import sys
from pathlib import Path
import os
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
import fasttext
import fasttext.util
from cs336_data.common import CS336_DATA_PATH
NSFW_MODEL_URL = "https://dolma-artifacts.org/fasttext_models/jigsaw_fasttext_bigrams_20230515/jigsaw_fasttext_bigrams_nsfw_final.bin"
TOXIC_MODEL_URL = "https://dolma-artifacts.org/fasttext_models/jigsaw_fasttext_bigrams_20230515/jigsaw_fasttext_bigrams_hatespeech_final.bin"

def ensure_model(path: Path, url: str):
    if not path.exists():
        print(f"Model not found at {path}, downloading from {url}...")
        os.system(f"wget -O {path} {url}")

# Classify whether the text contains NSFW content
def nsfw_classify(text: str):
    model_path = CS336_DATA_PATH / "jigsaw_fasttext_bigrams_nsfw_final.bin"
    ensure_model(model_path, NSFW_MODEL_URL)
    model = fasttext.load_model(str(model_path))

    max_nsfw_score = 0.01
    detected_label = "non-nsfw"

    for line in text.split("\n"):
        if line.strip():
            labels, scores = model.predict(line.strip(), k=1)
            score = float(scores[0])
            if labels[0] == "__label__nsfw":
                detected_label = "nsfw"
                max_nsfw_score = max(max_nsfw_score, score)
            else:
                max_nsfw_score = max(max_nsfw_score, 1.0 - score)

    return detected_label, round(max_nsfw_score, 4)

# Classify whether the text contains toxic speech
def toxic_speech_classify(text: str):
    model_path = CS336_DATA_PATH / "jigsaw_fasttext_bigrams_hatespeech_final.bin"
    ensure_model(model_path, TOXIC_MODEL_URL)
    model = fasttext.load_model(str(model_path))

    max_toxic_score = 0.01
    detected_label = "non-toxic"

    for line in text.split("\n"):
        if line.strip():
            labels, scores = model.predict(line.strip(), k=1)
            score = float(scores[0])
            if labels[0] == "__label__toxic":
                detected_label = "toxic"
                max_toxic_score = max(max_toxic_score, score)
            else:
                max_toxic_score = max(max_toxic_score, 1.0 - score)

    return detected_label, round(max_toxic_score, 4)
