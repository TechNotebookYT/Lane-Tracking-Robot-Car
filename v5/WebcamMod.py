import cv2
 
vCapture = cv2.VideoCapture(0) # Captures from USB Webcam

# Retrieves Image from Camera & Resizes
def getImg(imgSize=[480,240]):
    success, img = vCapture.read()
    img = cv2.resize(img,(imgSize[0],imgSize[1]))
    return img


def showImg(img, name):
    cv2.imshow(name,img)

# Camera Test Script
if __name__ == '__main__':
    while True:
        img = getImg()
        showImg(img, 'img')
        cv2.waitKey(50)