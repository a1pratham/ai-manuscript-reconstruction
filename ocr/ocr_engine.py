import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def run_ocr(image):

    # upscale image for better OCR accuracy
    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC
    )

    custom_config = r'--oem 3 --psm 6'

    data = pytesseract.image_to_data(
        image,
        config=custom_config,
        output_type=pytesseract.Output.DATAFRAME
    )

    # remove rows where text is NaN
    data = data.dropna(subset=["text"])

    # remove empty strings
    data = data[data["text"].str.strip() != ""]

    # convert confidence to float
    data["conf"] = data["conf"].astype(float)

    return data