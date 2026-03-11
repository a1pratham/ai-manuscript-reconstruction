import cv2

from preprocessing.image_cleaning import preprocess_image
from ocr.ocr_engine import run_ocr


image_path = "test.png"

processed = preprocess_image(image_path)

ocr_data = run_ocr(processed)

# show only important columns
ocr_data = ocr_data[["text", "conf", "line_num"]]

ocr_data = ocr_data.dropna()

print(ocr_data)