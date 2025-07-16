from MotorController import MotorController
import cv2
from LaneDetection import getLaneCurve
import WebcamMod
 
# Initialize MotorController
car = MotorController((2, 3, 4), (22, 27, 17), leftBias=1, rightBias=1)

# --- PID Controller State ---
previous_error = 0
integral = 0
# --------------------------
 
def main():
    global previous_error, integral

    # --- PID Constants (These will need tuning!) ---
    Kp = 0.4    # Proportional gain
    Ki = 0.001  # Integral gain
    Kd = 0.3    # Derivative gain
    # ---------------------------------------------

    base_speed = 30

    img = WebcamMod.getImg()
    error = getLaneCurve(img) # The error is the curve value from lane detection

    # PID Calculation
    integral += error
    derivative = error - previous_error
    turn_value = (Kp * error) + (Ki * integral) + (Kd * derivative)
    previous_error = error

    # Use the new steer method to control the car
    car.steer(speed=base_speed, turn=turn_value)

     
try: 
    if __name__ == '__main__':
        while True:
            main()
            cv2.waitKey(7) # Needed to display elements on screen
finally:
    car.stop() # Stops the Car
    car.exit() # Runs Pin Cleanup script