import cv2

def preprocess_image(image_path):

    image = cv2.imread(image_path)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # increase contrast
    gray = cv2.equalizeHist(gray)

    # remove noise
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # binary threshold
    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    return thresh