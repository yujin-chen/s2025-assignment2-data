#!/usr/bin/env python3
import sys
from pathlib import Path
import os
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
import fasttext
from cs336_data.common import CS336_DATA_PATH
LANG_ID_MODEL_PATH = CS336_DATA_PATH / "lid.176.bin"
LANG_ID_MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"

# Ensure model is available
def ensure_model(path: Path, url: str):
    if not path.exists():
        print(f"Language ID model not found at {path}, downloading from {url}...")
        os.system(f"wget -O {path} {url}")

# Check/download before loading
ensure_model(LANG_ID_MODEL_PATH, LANG_ID_MODEL_URL)

# Load the model
lang_id_model = fasttext.load_model(str(LANG_ID_MODEL_PATH))

# Predict language of the input text
def identify_language(text: str):
    labels, scores = lang_id_model.predict(text.replace('\n', ' '), k=1)  # top-1 prediction
    raw_label = labels[0]
    confidence = scores[0]

    lang_code = raw_label.replace("__label__", "")

    # Remap for simplified Chinese variants
    if lang_code.startswith("zh"):
        lang_code = "zh"

    return lang_code, float(confidence)