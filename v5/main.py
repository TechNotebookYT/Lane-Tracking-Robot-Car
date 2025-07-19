from MotorController import MotorController
import cv2
from LaneDetection import getLaneCurve
import WebcamMod
from ImageStreamer import ImageStreamer
 
# Initialize MotorController
car = MotorController((2, 3, 4), (22, 27, 17), leftBias=1, rightBias=1)

 
def main():
    img = WebcamMod.getImg()
    curveVal, frame = getLaneCurve(img)
    streamer.update_image(frame)
    
    threshold_to_turn = 20
    
    # Check to turn right
    if curveVal > threshold_to_turn:
        car.turnRight(speed=100)
        print("turnright")
    
    # Check to turn left
    elif curveVal < -threshold_to_turn:
        car.turnLeft(speed=100)
        print("turnleft")

    else:
        car.moveForward(speed=100)

try: 
    if __name__ == '__main__':
        streamer = ImageStreamer(port=8000)
        streamer.start()

        
        while True:
            main()
            # cv2.waitKey(7) # Needed to display elements on screen
finally:
    car.stop() # Stops the Car
    car.exit() # Runs Pin Cleanup script
    streamer.stop() # Stops the Image Streamer