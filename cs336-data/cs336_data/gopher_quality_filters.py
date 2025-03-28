import nltk
import re

nltk.download("punkt")

def gopher_quality_filter(text: str) -> bool:

    # Tokenize text into words
    words = nltk.word_tokenize(text)
    num_words = len(words)

    # Filter 1: Text must have between 50 and 100,000 words
    if num_words < 50 or num_words > 100000:
        return False

    # Calculate mean word length
    word_lengths = [len(word) for word in words if word.isalpha()]
    mean_word_length = sum(word_lengths) / len(word_lengths) if word_lengths else 0

    # Filter 2: Mean word length must be between 3 and 10 characters
    if mean_word_length < 3 or mean_word_length > 10:
        return False

    # Count lines that end with ellipses ("...")
    lines = text.split("\n")
    ellipsis_count = sum(1 for line in lines if line.strip().endswith("..."))

    # Filter 3: More than 30% of lines ending with "..." is low quality
    if len(lines) > 0 and (ellipsis_count / len(lines)) > 0.3:
        return False

    # Count words with at least one alphabetic character
    words_with_alpha = sum(1 for word in words if any(character.isalpha() for character in word))

    # Filter 4: At least 80% of words must contain at least one alphabetic character
    if num_words > 0 and (words_with_alpha / num_words) < 0.8:
        return False

    return True  
