import pandas as pd
import re
from datasets import load_dataset
from damage_generator import generate_synthetic_pair

print("Connecting to Hugging Face to stream Wikipedia text...")
# We use wikitext which is standard, high-quality Wikipedia articles
dataset = load_dataset("wikitext", "wikitext-103-raw-v1", split="train", streaming=True)

def clean_and_split_text(raw_text):
    """Removes weird Wikipedia formatting and splits into sentences."""
    # Remove titles and empty lines
    if raw_text.startswith(" = ") or len(raw_text.strip()) < 10:
        return []
    
    # Split paragraph into sentences by looking for periods followed by a space
    sentences = re.split(r'(?<=[.!?]) +', raw_text.strip())
    
    valid_sentences = []
    for s in sentences:
        words = s.split()
        # Only keep sentences that are a reasonable length (5 to 30 words)
        if 5 <= len(words) <= 30 and not bool(re.search(r'[@#^&*<>\/|]', s)):
            valid_sentences.append(s)
            
    return valid_sentences

# --- CONFIGURATION ---
TARGET_SENTENCE_COUNT = 10000  # Let's start with 10k to test it, then we can bump to 500k!

data_rows = []
print(f"Mining and corrupting {TARGET_SENTENCE_COUNT} sentences. Please wait...")

# Stream through the dataset
for item in dataset:
    sentences = clean_and_split_text(item['text'])
    
    for clean_sentence in sentences:
        # 1. Run our damage math
        clean, damaged = generate_synthetic_pair(clean_sentence)
        
        # 2. Save the pair
        data_rows.append({
            "input": damaged,
            "target": clean
        })
        
        if len(data_rows) % 2000 == 0:
            print(f"Processed {len(data_rows)} / {TARGET_SENTENCE_COUNT} sentences...")
            
        if len(data_rows) >= TARGET_SENTENCE_COUNT:
            break
            
    if len(data_rows) >= TARGET_SENTENCE_COUNT:
        break

# 3. Save to a Pandas DataFrame and export to CSV
print("\nCreating Pandas DataFrame...")
df = pd.DataFrame(data_rows)

output_file = "datasets/synthetic_training_data.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"\nSuccess! Saved {len(df)} training pairs to {output_file}.")
print("Here is a sneak peek at your new dataset:")
print(df.head())