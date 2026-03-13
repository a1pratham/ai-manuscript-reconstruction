import cv2

def segment_lines(image):
    # INCREASED from 40 to 150 to bridge large horizontal gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (150, 5)) 

    dilated = cv2.dilate(image, kernel, iterations=1)

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # ... (keep the rest of your segment_lines code exactly the same)

    boxes = []

    for c in contours:

        x, y, w, h = cv2.boundingRect(c)

        if h < 20 or w < 50:
            continue

        boxes.append((x, y, w, h))

    # sort first by Y, then by X
    boxes = sorted(boxes, key=lambda b: (b[1], b[0]))

    line_images = []

    padding = 5

    for x, y, w, h in boxes:

        y1 = max(y - padding, 0)
        y2 = y + h + padding
        x1 = max(x - padding, 0)
        x2 = x + w + padding

        line = image[y1:y2, x1:x2]

        line_images.append(line)

    return line_images