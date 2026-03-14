import cv2
import pandas as pd

from preprocessing.image_cleaning import preprocess_image
from preprocessing.line_segmentation import segment_lines
from ocr.ocr_engine import run_ocr
from ocr.gap_detection import detect_gaps

image = cv2.imread("test.png")

processed = preprocess_image(image)

lines = segment_lines(processed)

all_ocr = []

# run OCR for every line
for i, line in enumerate(lines):

    df = run_ocr(line)
    
    # Make sure the dataframe isn't completely empty before appending
    if df is not None and not df.empty:
        # add line number so we can group crops later
        df["line_id"] = i
        all_ocr.append(df)

if all_ocr:
    # combine OCR results
    full_df = pd.concat(all_ocr)

    # 1. Safely build the sorting columns
    # We prioritize Tesseract's natural reading order over a blind X-coordinate sort
    sort_cols = ["line_id"]
    for col in ["block_num", "par_num", "line_num", "word_num"]:
        if col in full_df.columns:
            sort_cols.append(col)
        elif col == "word_num" and "left" in full_df.columns:
            # Fallback if standard pytesseract columns aren't perfectly matching
            sort_cols.append("left")

    # 2. Sort words correctly to prevent "zippering"
    full_df = full_df.sort_values(sort_cols)

    print("\n--- GAP TAGGED TEXT ---\n")

    # Call detect_gaps
    gap_text = detect_gaps(full_df, word_threshold=45, char_threshold=75)

    print(gap_text)
else:
    print("No text or lines detected in the image.")