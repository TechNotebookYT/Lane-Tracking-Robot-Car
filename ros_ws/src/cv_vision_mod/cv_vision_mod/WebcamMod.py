import cv2
import numpy as np
import utils

def getLaneCurve(img):
    
    thresholdImage = utils.thresholding(img)

    h, w, c = img.shape
    points = utils.initWarpPointsArray([102, 80, 20, 214])
    imgWarp = utils.warpImg(thresholdImage, points, w, h)

    cv2.imshow('warp', imgWarp)

    curve = check_white_pixels(thresholdImage)

    print(curve)
    return curve 


def check_white_pixels(frame):
    
    # Calculate the height of the top 2 thirds
    height = frame.shape[0] * 2 // 3
    
    # Crop the image to only include the top 2 thirds
    cropped = frame[:height, :]
    
    # Calculate the width of each fifth
    width = cropped.shape[1] // 5
    
    # Split the image into fifths
    left_2_fifths = frame[:, :width*2]
    right_2_fifths = frame[:, -width*2:]
    
    # Calculate the number of non-zero pixels in each side
    left_count = np.count_nonzero(left_2_fifths)
    right_count = np.count_nonzero(right_2_fifths)
    
    # Calculates the % of each region is comprised of white pixels
    left_percent = left_count / (left_2_fifths.size)
    right_percent = right_count / (right_2_fifths.size)

    # Balance: Value between -100 and 100 that shows the distribution of white pixels
    balance = int((right_percent-left_percent)*100)

    
    return balance

# Module Testing Code
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    
    while True:
        success, img = cap.read()
        if not success:
            continue
        img = cv2.resize(img, (480, 240))
        getLaneCurve(img)
        cv2.imshow('vid', img)
        cv2.waitKey(1)