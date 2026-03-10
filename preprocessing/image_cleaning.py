import cv2

def preprocess_image(image_path):

    # load image
    image = cv2.imread(image_path)

    # convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # remove noise
    denoised = cv2.medianBlur(gray, 3)

    # adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh