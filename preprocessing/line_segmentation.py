import cv2
import numpy as np

def segment_lines(image):

    # invert image so text becomes white
    inverted = 255 - image

    # sum pixels horizontally
    horizontal_projection = np.sum(inverted, axis=1)

    threshold = np.max(horizontal_projection) * 0.1

    lines = []
    start = None

    for i, value in enumerate(horizontal_projection):

        if value > threshold and start is None:
            start = i

        elif value <= threshold and start is not None:
            end = i

            if end - start > 10:
                line = image[start:end, :]
                lines.append(line)

            start = None

    return lines