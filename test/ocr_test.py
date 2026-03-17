import pytesseract
import cv2

# path to tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# load image
image = cv2.imread("test.png")

# convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# run OCR
text = pytesseract.image_to_string(gray)

print("OCR RESULT:")
print(text)