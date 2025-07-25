from MotorController import MotorController
import cv2
from LaneDetection import getLaneCurve, PID_control
import WebcamMod
from ImageStreamer import ImageStreamer
import time
from utils import print_slider
 
# Initialize MotorController
# --- ⚙️ PIN CONFIGURATION ---
# !!! IMPORTANT !!!
# Replace these placeholder pin numbers with the actual BCM pin numbers (https://pinout.xyz)
# you have connected to your motor driver.
# Format: (Enable Pin, Forward Pin, Reverse Pin)
car = MotorController((2, 3, 4), (22, 27, 17), leftBias=1, rightBias=1)

def main(movement_enabled=False):
    img = WebcamMod.getImg() # Get image from WebcamMod module
    curveVal, frame = getLaneCurve(img) # calculate lane curve
    streamer.update_image(frame)

    # print(curveVal)
    steer_val = PID_control(curveVal, reset = (not movement_enabled))

    print_slider(steer_val) # Print slider to show detection

    if movement_enabled:
        car.steer(30, steer_val)

try: 
    if __name__ == '__main__':
        streamer = ImageStreamer(port=8000)
        streamer.start()
        
        # Read camera for the first 5 seconds without motor control
        start_time = time.time()
        print("Reading camera for 5 seconds...")
        while time.time() - start_time < 5:
            main() # Call main to update image streamer
            time.sleep(0.01) # Small delay to avoid busy-waiting

        print("Motor control enabled.")
        
        while True:
            main(movement_enabled=True)
            time.sleep(0.01) # Small delay to avoid busy-waiting
finally:
    car.stop() # Stops the Car
    time.sleep(0.2)
    # car.exit() # ! Runs Pin Cleanup script (for some reason my pi acts weird when this line run)
    streamer.stop() # Stops the Image Streamer  