import cv2
import numpy as np

def gaussianBlur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def generate_avg_slope(lines_list):
    slopes = []
    print(lines_list)
    if len(lines_list) == 0:
        return None
    for line in lines_list:
        x1, y1, x2, y2 = line[0]
        if (x2-x1) == 0:
            slopes.append((y2-y1)/(x2+0.01-x1))
        else:
            slopes.append((y2-y1)/(x2-x1))
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
    avg_slope = sum(slopes)/len(slopes)
    return avg_slope


def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(75, height), (220, height), (160, 125)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)
    return cv2.bitwise_and(mask, image)

def car_navigation(slope):
    if abs(slope) < 30:
        if slope > 0:
            print("turn right")
        else:
            print("turn left")

img = cv2.imread('img4.jpg')
blur = gaussianBlur(img, 3)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 75, 180) #70-150 is the threshold
masked = region_of_interest(edges)

lines = cv2.HoughLinesP(masked, 1, np.pi/180, 10, maxLineGap=50)
print(generate_avg_slope(lines))

car_navigation(generate_avg_slope(lines))
cv2.imshow("Edges", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
