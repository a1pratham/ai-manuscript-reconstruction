import cv2

from preprocessing.image_cleaning import preprocess_image
from preprocessing.line_segmentation import segment_lines

image_path = "test.png"

processed = preprocess_image(image_path)

lines = segment_lines(processed)

print("Lines detected:", len(lines))

for i, line in enumerate(lines):

    cv2.imshow(f"Line {i}", line)

cv2.waitKey(0)
cv2.destroyAllWindows()