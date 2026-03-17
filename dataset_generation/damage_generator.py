import random

def remove_random_chars(text, corruption_rate=0.15):
    words = text.split()
    damaged_words = []
    
    for word in words:
        if len(word) > 3 and random.random() < corruption_rate:
            char_idx = random.randint(1, len(word) - 2) 
            word = word[:char_idx] + "_" + word[char_idx+1:]
        damaged_words.append(word)
        
    # Fallback: if random chance missed everything, force at least one character to break
    result = " ".join(damaged_words)
    if result == text and len(words) > 0:
        idx = random.randint(0, len(words)-1)
        if len(words[idx]) > 3:
            char_idx = random.randint(1, len(words[idx]) - 2)
            words[idx] = words[idx][:char_idx] + "_" + words[idx][char_idx+1:]
            return " ".join(words)
            
    return result

def mask_random_words(text, corruption_rate=0.20):
    words = text.split()
    
    for i in range(len(words)):
        if random.random() < corruption_rate:
            words[i] = "[WORD_GAP]"
            
    # Fallback: guarantee at least one gap
    if "[WORD_GAP]" not in words and len(words) > 0:
        words[random.randint(0, len(words)-1)] = "[WORD_GAP]"
            
    return " ".join(words)

def drop_phrase_spans(text):
    """Replaces a continuous chunk of 2-4 words with [LINE_GAP]."""
    words = text.split()
    
    if len(words) < 5:
        return text 
        
    # We removed the random chance to skip. If this function is called, it WILL drop a span.
    start_idx = random.randint(0, len(words) - 4)
    span_length = random.randint(2, 4)
    
    words[start_idx : start_idx + span_length] = ["[LINE_GAP]"]
    return " ".join(words)

def generate_synthetic_pair(clean_text):
    damage_type = random.choice(['char', 'word', 'span', 'mixed'])
    
    if damage_type == 'char':
        damaged = remove_random_chars(clean_text)
    elif damage_type == 'word':
        damaged = mask_random_words(clean_text)
    elif damage_type == 'span':
        damaged = drop_phrase_spans(clean_text)
    else:
        damaged = mask_random_words(clean_text, corruption_rate=0.1)
        damaged = remove_random_chars(damaged, corruption_rate=0.1)
        
    return clean_text, damaged


if __name__ == "__main__":
    # Let's test it with a clean sentence
    sample_sentence = "The king of England ruled wisely for many years before the great war."
    
    print("--- SYNTHETIC DAMAGE GENERATOR ---")
    print(f"ORIGINAL: {sample_sentence}\n")
    
    for i in range(5):
        clean, damaged = generate_synthetic_pair(sample_sentence)
        print(f"Target : {clean}")
        print(f"Input  : {damaged}")
        print("-" * 50)