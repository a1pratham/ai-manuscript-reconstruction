import pandas as pd

def detect_gaps(df, char_threshold=70, word_threshold=40, physical_gap_threshold=80):
    result = []
    
    prev_right = None
    prev_line = None

    # 1. DYNAMICALLY calculate the median width of a word in THIS specific image
    # We use median instead of mean so tiny words like "a" or "I" don't skew the math
    valid_words = df[df["text"].str.strip() != ""]
    if not valid_words.empty:
        median_word_width = valid_words["width"].median()
    else:
        median_word_width = 50 # Fallback just in case the page is totally blank

    for _, row in df.iterrows():
        word = str(row["text"]).strip()
        if not word or word == "nan":
            continue

        conf = float(row["conf"])
        left = int(row["left"])
        width = int(row["width"])
        line = int(row["line_id"])

        if prev_line is not None and line != prev_line:
            result.append("\n")
            prev_right = None

        # 2. Use the dynamic width for the estimation
        if prev_right is not None:
            gap = left - prev_right
            
            if gap > physical_gap_threshold:
                # Divide the gap by the ACTUAL median word width of the document
                # Using round() instead of // gives a much more accurate estimate
                estimated_missing = max(1, round(gap / median_word_width))
                
                if estimated_missing > 1:
                    result.append(f"[{estimated_missing}_WORD_GAPS]")
                else:
                    result.append("[WORD_GAP]")

        if conf < word_threshold:
            result.append("[WORD_GAP]") 
        elif conf < char_threshold:
            result.append(word[:-1] + "[CHAR_GAP]")
        else:
            result.append(word)

        prev_right = left + width
        prev_line = line

    final_text = " ".join(result)
    final_text = final_text.replace(" \n ", "\n").replace("\n ", "\n")
    
    return final_text