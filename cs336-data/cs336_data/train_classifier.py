#!/usr/bin/env python3
import sys
from pathlib import Path
CURRENT_FILE = Path(__file__).resolve().parents[1]
sys.path.append(str(CURRENT_FILE))
import fasttext
from cs336_data.common import KOA_SCRATCH_PATH

# Paths to dataset
TRAIN_FILE = KOA_SCRATCH_PATH / "quality_train.txt"
VALID_FILE = KOA_SCRATCH_PATH / "quality_valid.txt"
TEST_FILE = KOA_SCRATCH_PATH / "quality_test.txt"
MODEL_PATH = KOA_SCRATCH_PATH / "quality_classifier.bin"

# Train model with validation set
model = fasttext.train_supervised(
    input=str(TRAIN_FILE),
    autotuneValidationFile=str(VALID_FILE),
    autotuneDuration=600
)


# Save model
model.save_model(str(MODEL_PATH))
print(f"Model saved to {MODEL_PATH}")


# Evaluate on test set
test_result = model.test(str(TEST_FILE))
print(f"Test accuracy: {test_result[1]:.4f}")
