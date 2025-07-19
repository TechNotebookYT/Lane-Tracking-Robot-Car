from MotorController import MotorController
import cv2
from LaneDetection import getLaneCurve
import WebcamMod
from ImageStreamer import ImageStreamer
import time
 
# Initialize MotorController
car = MotorController((2, 3, 4), (22, 27, 17), leftBias=1, rightBias=1)

 
def main():
    img = WebcamMod.getImg()
    curveVal, frame = getLaneCurve(img)
    streamer.update_image(frame)
    
    threshold_to_turn = 30
    
    # Check to turn right
    if curveVal > threshold_to_turn:
        car.turnRight(speed=35)
        # time.sleep(0.03)
        print("turnright")
    
    # Check to turn left
    elif curveVal < -threshold_to_turn:
        car.turnLeft(speed=35)
        # time.sleep(0.03)
        print("turnleft")

    else:
        car.moveForward(speed=30)

try: 
    if __name__ == '__main__':
        streamer = ImageStreamer(port=8000)
        streamer.start()
        print("5 seconds til robot starts")
        time.sleep(5)
        
        while True:
            main()
            # time.sleep(0.05)
            # cv2.waitKey(7) # Needed to display elements on screen
finally:
    car.stop() # Stops the Car
    time.sleep(0.2)
    # car.exit() # Runs Pin Cleanup script
    streamer.stop() # Stops the Image Streamer