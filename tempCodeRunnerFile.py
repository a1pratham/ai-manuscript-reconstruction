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

    # add line number so we can sort later
    df["line_id"] = i

    all_ocr.append(df)

# combine OCR results
full_df = pd.concat(all_ocr)

# sort words correctly
full_df = full_df.sort_values(["line_id", "left"])

print("\n--- GAP TAGGED TEXT ---\n")

# Tweak the 80 to match the scale of your specific test.png
gap_text = detect_gaps(full_df, physical_gap_threshold=80)

print(gap_text)