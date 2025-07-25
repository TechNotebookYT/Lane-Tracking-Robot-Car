import cv2
import numpy as np
import utils


def getLaneCurve(img):
    """
    Get Lane Curve
    --
    This module calculates the lane curve from an input image.
    """
    thresholdImage = utils.thresholding(img)

    h, w, c = img.shape
    points = utils.initWarpPointsArray([76, 60, 15, 161])
    imgWarp = utils.warpImg(thresholdImage, points, w, h)

    # cv2.imshow('warp', imgWarp)
    # curve = check_white_pixels(threshodlImage)
    curve = get_lane_error_norm(imgWarp)

    # print(curve)
    return curve, imgWarp


def get_lane_error(thresholded_img):
    """
    Calculates the horizontal error from the center of the lane using the centroid method.
    This value is the input for a PID controller.

    Args:
        warped_thresholded_img: A black and white, warped image where the lane is white.

    Returns:
        error (int): Positive means the lane is to the right of the image center, negative means it's to the left.
    """
    # 1. Define a Region of Interest (a horizontal slice of the image)
    height, width = thresholded_img.shape

    # We will analyze the slice between 60% and 80% from the top of the image
    roi_start_y = int(height * 0.6)
    roi_end_y = int(height * 0.8)
    roi = thresholded_img[roi_start_y:roi_end_y, :]

    # 2. Calculate the centroid of the white pixels in the ROI
    M = cv2.moments(roi)

    if M["m00"] != 0:
        # cX is the horizontal center of the lane in the ROI
        cX = int(M["m10"] / M["m00"])
    else:
        # No lane was detected in the ROI.
        # You can return 0 or a previous error value.
        return 0

    # 3. Calculate the error from the image center
    image_center_x = width // 2
    error = cX - image_center_x

    return error

def get_lane_error_norm(thresholded_img, roi_top=0.6, roi_bot=0.8, default=0.0):
    """
    Returns a normalized lateral error in [-1.0, 1.0].
    +1  -> lane centroid all the way at the right edge
    -1  -> lane centroid all the way at the left edge

    Args:
        thresholded_img (np.ndarray): Binary (0/255) warped image; lane is white.
        roi_top (float): Top of ROI as a fraction of image height.
        roi_bot (float): Bottom of ROI as a fraction of image height.
        default (float): Value to return if no lane pixels are found.

    Returns:
        float: normalized error in [-1, 1]
    """
    import cv2
    import numpy as np

    h, w = thresholded_img.shape
    y0, y1 = int(h * roi_top), int(h * roi_bot)
    roi = thresholded_img[y0:y1, :]

    M = cv2.moments(roi)
    if M["m00"] == 0:
        return float(default)

    cX = M["m10"] / M["m00"]           # centroid x (float)
    center = (w - 1) / 2.0             # exact pixel center (works for even/odd)
    raw_error = cX - center

    max_mag = center                    # max possible |error|
    norm_error = raw_error / max_mag    # now in [-1, 1] (or very close)

    # numerical safety clamp
    return float(np.clip(norm_error, -1.0, 1.0))

def check_white_pixels(frame):
    """
    (OLD) Calculates the balance of white pixels in the left and right two-fifths of the frame.

    Args:
        frame (numpy.ndarray): The input image frame (grayscale, thresholded).

    Returns:
        int: A value between -100 and 100 indicating the balance of white pixels.
             Positive values mean more white pixels on the right, negative on the left.
    """

    # Calculate the height of the top 2 thirds
    height = frame.shape[0] * 2 // 3

    # Crop the image to only include the top 2 thirds
    cropped = frame[:height, :]

    # Calculate the width of each fifth
    width = cropped.shape[1] // 5

    # Split the image into fifths
    left_2_fifths = frame[:, : width * 2]
    right_2_fifths = frame[:, -width * 2 :]

    # Calculate the number of non-zero pixels in each side
    left_count = np.count_nonzero(left_2_fifths)
    right_count = np.count_nonzero(right_2_fifths)

    # Calculates the % of each region is comprised of white pixels
    left_percent = left_count / (left_2_fifths.size)
    right_percent = right_count / (right_2_fifths.size)

    # Balance: Value between -100 and 100 that shows the distribution of white pixels
    balance = int((right_percent - left_percent) * 100)

    return balance



previous_error = 0.0
integral = 0.0
def PID_control(error_value: float, dt: float = 0.05, reset: bool = False) -> float:
    """
    PID on a normalized error in [-1, 1]. Returns steering in [-1, 1].

    Args:
        error_value (float): normalized error (-1 = lane far left, +1 = far right)
        dt (float): time since last call (seconds)
        reset (bool): true to zero integral/derivative state

    Returns:
        float: steering command in [-1, 1]
    """
    import math
    global previous_error, integral

    if reset:
        print("reset")
        previous_error = 0.0
        integral = 0.0

    # --- Tunable gains (normalized units) ---
    Kp = 0.9

    Ki = 0.1
    
    Kd = 0.1

    # --- Proportional ---
    P = error_value

    # --- Integral (with anti-windup clamp) ---
    integral += error_value * dt
    I_MAX = 2.0  # adjust as needed
    integral = max(-I_MAX, min(I_MAX, integral))
    I = integral

    # --- Derivative (simple form; consider filtering if noisy) ---
    D = (error_value - previous_error) / dt if dt > 0 else 0.0

    # PID sum
    u = Kp * P + Ki * I + Kd * D

    # Save state
    previous_error = error_value

    # Clamp output to actuator range
    return max(-1.0, min(1.0, u))

 

# Module Testing Code
# ! only works in non-headless versions (use the imagestreamer module if in headless mode)
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.resize(img, (480, 240))
        getLaneCurve(img)
        cv2.imshow("vid", img)
        cv2.waitKey(1)
