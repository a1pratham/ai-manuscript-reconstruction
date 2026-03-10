import cv2
from preprocessing.image_cleaning import preprocess_image

image_path = "test.png"

processed = preprocess_image(image_path)

cv2.imshow("Processed Image", processed)
cv2.waitKey(0)
cv2.destroyAllWindows()