# import pandas as pd
# import re
# from spellchecker import SpellChecker # NEW IMPORT

# # Initialize the dictionary
# spell = SpellChecker()
# # Add custom words that the dictionary shouldn't delete
# # The future setup
# # def detect_gaps(df, custom_vocab=[], char_threshold=75, word_threshold=45):
# #     spell = SpellChecker()
# #     if custom_vocab:
# #         spell.word_frequency.load_words(custom_vocab)
#     # ... the rest of your working code

# def detect_gaps(df, char_threshold=75, word_threshold=45, physical_gap_threshold=80):
#     result = []
    
#     prev_right = None
#     prev_line = None

#     valid_words = df[df["text"].str.strip() != ""]
#     if not valid_words.empty:
#         median_word_width = valid_words["width"].median()
#     else:
#         median_word_width = 50 

#     for _, row in df.iterrows():
#         word = str(row["text"]).strip()
        
#         if not word or word == "nan" or re.fullmatch(r'[_\-\|\[\]/\\]+', word):
#             continue

#         # Clean off any box lines or hallucinated punctuation like that rogue "!"
#         # We target specific garbage like |, _, [, ], and ! but leave commas alone
#         clean_word = re.sub(r'^[_\-\|\[\]/\\!]+|[_\-\|\[\]/\\!]+$', '', word)
        
#         if not clean_word:
#             continue

#         conf = float(row["conf"])
#         left = int(row["left"])
#         width = int(row["width"])
        
#         tess_line = int(row.get("line_num", 0))
#         current_line_id = f"{row.get('line_id', 0)}_{tess_line}"

#         if prev_line is not None and current_line_id != prev_line:
#             result.append("\n")
#             prev_right = None

#         if prev_right is not None:
#             gap = left - prev_right
            
#             if gap > physical_gap_threshold:
#                 estimated_missing = max(1, round(gap / median_word_width))
                
#                 if estimated_missing > 1:
#                     result.append(f"[{estimated_missing}_WORD_GAPS]")
#                 else:
#                     result.append("[WORD_GAP]")

#         if conf < word_threshold:
#             estimated_damaged_words = max(1, round(width / median_word_width))
#             if estimated_damaged_words > 1:
#                 result.append(f"[{estimated_damaged_words}_WORD_GAPS]")
#             else:
#                 result.append("[WORD_GAP]")
                
#         elif conf < char_threshold:
#             # NEW LOGIC: Check if it's a real word.
#             # If it's gibberish like "ka" or "thea", nuke it into a WORD_GAP.
#             if clean_word.lower() in spell:
#                 result.append(clean_word[:-1] + "[CHAR_GAP]")
#             else:
#                 result.append("[WORD_GAP]")
#         else:
#             result.append(clean_word)

#         prev_right = left + width
#         prev_line = current_line_id

#     final_text = " ".join(result)
    
#     final_text = re.sub(r' +', ' ', final_text) 
#     final_text = re.sub(r'(\[WORD_GAP\]\s*)+', '[WORD_GAP] ', final_text)
#     final_text = final_text.replace(" \n ", "\n").replace("\n ", "\n").replace(" \n", "\n")
    
#     return final_text.strip()



# .............................................................................

import pandas as pd
import re
from spellchecker import SpellChecker

def detect_gaps(df, custom_dict_path=None, char_threshold=75, word_threshold=45, physical_gap_threshold=80):
    result = []
    
    # 1. DYNAMIC DICTIONARY LOADING
    if custom_dict_path:
        # Turn off Modern English and load the historical text file
        spell = SpellChecker(language=None)
        spell.word_frequency.load_text_file(custom_dict_path)
    else:
        # Default to Modern English (with your custom scientific words)
        spell = SpellChecker()
        spell.word_frequency.load_words(['turritopsis', 'dohrnii'])

    prev_right = None
    prev_line = None

    valid_words = df[df["text"].str.strip() != ""]
    if not valid_words.empty:
        median_word_width = valid_words["width"].median()
    else:
        median_word_width = 50 

    for _, row in df.iterrows():
        word = str(row["text"]).strip()
        
        if not word or word == "nan" or re.fullmatch(r'[_\-\|\[\]/\\]+', word):
            continue

        # This surgical regex safely ignores garbage but KEEPS historical letters (þ, ð, æ)
        clean_word = re.sub(r'^[_\-\|\[\]/\\!]+|[_\-\|\[\]/\\!]+$', '', word)
        
        if not clean_word:
            continue

        conf = float(row["conf"])
        left = int(row["left"])
        width = int(row["width"])
        
        tess_line = int(row.get("line_num", 0))
        current_line_id = f"{row.get('line_id', 0)}_{tess_line}"

        if prev_line is not None and current_line_id != prev_line:
            result.append("\n")
            prev_right = None

        if prev_right is not None:
            gap = left - prev_right
            
            if gap > physical_gap_threshold:
                estimated_missing = max(1, round(gap / median_word_width))
                if estimated_missing > 1:
                    result.append(f"[{estimated_missing}_WORD_GAPS]")
                else:
                    result.append("[WORD_GAP]")

        if conf < word_threshold:
            estimated_damaged_words = max(1, round(width / median_word_width))
            if estimated_damaged_words > 1:
                result.append(f"[{estimated_damaged_words}_WORD_GAPS]")
            else:
                result.append("[WORD_GAP]")
                
        elif conf < char_threshold:
            # 2. Check the dynamic dictionary
            if clean_word.lower() in spell:
                result.append(clean_word[:-1] + "[CHAR_GAP]")
            else:
                result.append("[WORD_GAP]")
        else:
            result.append(clean_word)

        prev_right = left + width
        prev_line = current_line_id

    final_text = " ".join(result)
    final_text = re.sub(r' +', ' ', final_text) 
    final_text = re.sub(r'(\[WORD_GAP\]\s*)+', '[WORD_GAP] ', final_text)
    final_text = final_text.replace(" \n ", "\n").replace("\n ", "\n").replace(" \n", "\n")
    
    return final_text.strip()