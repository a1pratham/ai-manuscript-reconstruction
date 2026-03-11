import cv2

def segment_lines(image):

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,5))

    dilated = cv2.dilate(image, kernel, iterations=1)

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    line_images = []

    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])

    for c in contours:

        x, y, w, h = cv2.boundingRect(c)

        if h > 20:
            line = image[y:y+h, x:x+w]
            line_images.append(line)

    return line_images