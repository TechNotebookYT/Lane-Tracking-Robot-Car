import cv2

# open camera once
vCapture = cv2.VideoCapture(0)
# request 360×240 frames directly
vCapture.set(cv2.CAP_PROP_FRAME_WIDTH, 360)
vCapture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

def getImg():
    success, img = vCapture.read()
    if not success:
        return None
    return img

# Camera Test Script
if __name__ == '__main__':
    pass
    # while True:
    #     img = getImg()
    #     showImg(img, 'img')
    #     cv2.waitKey(50)