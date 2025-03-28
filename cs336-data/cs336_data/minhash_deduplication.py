import os
import re
import random
import hashlib
import unicodedata
from typing import List

# Normalize text by lowercasing, removing punctuation, whitespace, and accents
def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    return unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')

# Generate word-level n-grams from normalized text
def generate_ngrams(text: str, n: int) -> set:
    words = text.split()
    return {' '.join(words[i:i+n]) for i in range(len(words)-n+1)}

# Generate a minhash signature vector from a set of n-grams
def minhash_signature(ngrams: set, hash_funcs: List) -> List[int]:
    return [min(h(ng) for ng in ngrams) for h in hash_funcs]

# Split the minhash signature into bands for LSH bucketing
def lsh_bands(signature: List[int], bands: int) -> List[tuple]:
    r = len(signature) // bands
    return [tuple(signature[i*r:(i+1)*r]) for i in range(bands)]

# Compute Jaccard similarity between two sets
def jaccard(set1: set, set2: set) -> float:
    return len(set1 & set2) / len(set1 | set2) if set1 or set2 else 0.0

# Generate k independent hash functions
def generate_hash_functions(k: int):
    seeds = [random.randint(0, 2**32 - 1) for _ in range(k)]
    return [lambda x, s=s: int(hashlib.md5((x + str(s)).encode()).hexdigest(), 16) for s in seeds]

# Main deduplication function using MinHash + LSH
def minhash_deduplication(
    files: List[os.PathLike],
    num_hashes: int,
    num_bands: int,
    ngram_len: int,
    threshold: float,
    output_dir: os.PathLike
):
    os.makedirs(output_dir, exist_ok=True) 

    hash_funcs = generate_hash_functions(num_hashes)  

    docs = []
    for path in files: 
        with open(path, 'r', encoding='utf-8') as f:
            raw = f.read()
        ngrams = generate_ngrams(normalize_text(raw), ngram_len)
        sig = minhash_signature(ngrams, hash_funcs)
        bands = lsh_bands(sig, num_bands)
        docs.append({'path': path, 'text': raw, 'ngrams': ngrams, 'sig': sig, 'bands': bands})

    buckets, parent = {}, list(range(len(docs))) 

    # Union-find: find root
    def find(x):  
        parent[x] = parent[x] if parent[x] == x else find(parent[x])
        return parent[x]
    # Union-find: merge sets
    def union(x, y):  
        parent[find(x)] = find(y)

    # Fill LSH buckets
    for i, doc in enumerate(docs):  
        for b in doc['bands']:
            buckets.setdefault(b, []).append(i)

    # Compare candidate pairs via Jaccard
    for ids in buckets.values():  
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                idx1, idx2 = ids[i], ids[j]
                sim = jaccard(docs[idx1]['ngrams'], docs[idx2]['ngrams'])
                if sim >= threshold:
                    union(idx1, idx2)
    # Group documents by connected components
    clusters = {}  
    for i in range(len(docs)):
        root = find(i)
        clusters.setdefault(root, []).append(i)
        
    # Write one random file per cluster
    written_paths = set()  
    for group in clusters.values():
        keep = random.choice(group)
        output_path = os.path.join(output_dir, os.path.basename(docs[keep]['path']))
        while output_path in written_paths:
            output_path = os.path.join(output_dir, f"{random.randint(0, 1e9)}.txt")
        written_paths.add(output_path)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(docs[keep]['text'])
