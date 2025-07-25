import cv2
import numpy as np

# Color-based Thresholding mask
def thresholding(img):
    grayscale = cv2.cvtColor(img, cv2. COLOR_BGR2GRAY)
    lowerThreshold = 0
    upperThreshold = 100
    mask = cv2.inRange(grayscale, lowerThreshold, upperThreshold)
    return mask

# Warps the Image
def warpImg(img, points, w, h, inv=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    
    imgWarp = cv2.warpPerspective(img, matrix, (w, h))
    return imgWarp

# Initializes the Array of points needed for warp
def initWarpPointsArray(values, wT=360, hT=240):
    widthTop = values[0]
    heightTop = values[1]
    widthBottom = values[2]
    heightBottom = values[3]
    
    return np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])

def print_slider(value):
    """
    Prints a text-based slider to visualize a value between -1 and 1.

    Args:
        value (float): A number between -1.0 (left) and 1.0 (right).
    """
    # Ensure the value is clamped between -1 and 1
    value = max(-1.0, min(1.0, value))

    # Define the appearance of the slider
    bar_width = 25  # Total characters for the bar (use an odd number for a perfect center)
    filler_char = '.'
    indicator_char = '|'

    # Map the value from the [-1, 1] range to an index in the bar
    # 1. Normalize the value to a [0, 1] range
    normalized_value = (value + 1) / 2
    # 2. Scale to the bar's width and round to the nearest whole number
    indicator_pos = round(normalized_value * (bar_width - 1))

    # Create the slider string
    bar_list = [filler_char] * bar_width
    bar_list[indicator_pos] = indicator_char
    bar_string = "".join(bar_list)
    
    # Print the final result, formatting the value to two decimal places
    print(f"<{bar_string}> {{{value:.2f}}}")