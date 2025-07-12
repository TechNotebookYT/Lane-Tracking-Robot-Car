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
def initWarpPointsArray(values, wT=480, hT=240):
    widthTop = values[0]
    heightTop = values[1]
    widthBottom = values[2]
    heightBottom = values[3]
    
    return np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])