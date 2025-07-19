"""
This module handles the motor control for the robot.

It also provides you with manual robot control functionality.
To use this feature, run this file as a script.
"""

import RPi.GPIO as GPIO
import curses
import time

class MotorController():
    """
    MOTOR CONTROL
    --
    This method contains functions to move the car in different directions
    """

    # Initialize Pin Setup
    def __init__(self, leftMotors, rightMotors, leftBias=1, rightBias=1):
        self.leftMotorsEnable, self.leftMotorsForward, self.leftMotorsReverse = leftMotors
        self.rightMotorsEnable, self.rightMotorsForward, self.rightMotorsReverse = rightMotors

        self.leftBias = leftBias
        self.rightBias = rightBias

        self.setup()

    # Sets the pinmode as well as the output pins
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False) # Disable GPIO warnings

        GPIO.setup(self.leftMotorsEnable, GPIO.OUT)
        GPIO.setup(self.rightMotorsEnable, GPIO.OUT)
        
        GPIO.setup(self.leftMotorsForward, GPIO.OUT)
        GPIO.setup(self.leftMotorsReverse, GPIO.OUT)
        GPIO.setup(self.rightMotorsForward, GPIO.OUT)
        GPIO.setup(self.rightMotorsReverse, GPIO.OUT)

        self.leftMotorsPWM = GPIO.PWM(self.leftMotorsEnable, 100);
        self.rightMotorsPWM = GPIO.PWM(self.rightMotorsEnable, 100);

        self.rightMotorsPWM.start(0);
        self.leftMotorsPWM.start(0);

    # Moves all wheels forward
    def moveForward(self, speed=50):
        dutyCycle = int(speed * self.leftBias)
        self.leftMotorsPWM.ChangeDutyCycle(dutyCycle)
        self.rightMotorsPWM.ChangeDutyCycle(speed)

        GPIO.output(self.leftMotorsForward, True)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, True)
        GPIO.output(self.rightMotorsReverse, False)

    # Moves all wheels in reverse
    def moveReverse(self, speed=50):
        dutyCycle = int(speed * self.leftBias)
        self.leftMotorsPWM.ChangeDutyCycle(dutyCycle)
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*self.rightBias))

        GPIO.output(self.leftMotorsForward, False)
        GPIO.output(self.leftMotorsReverse, True)
        GPIO.output(self.rightMotorsForward, False)
        GPIO.output(self.rightMotorsReverse, True)

    # Turns left on the spot (zero-point turn)
    def turnLeft(self, speed=50):
        dutyCycle = int(speed * self.leftBias)
        self.leftMotorsPWM.ChangeDutyCycle(dutyCycle)
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*self.rightBias))

        # Left motors reverse, Right motors forward
        GPIO.output(self.leftMotorsForward, False)
        GPIO.output(self.leftMotorsReverse, True)
        GPIO.output(self.rightMotorsForward, True)
        GPIO.output(self.rightMotorsReverse, False)

    # Turns right on the spot (zero-point turn)
    def turnRight(self, speed=50):
        dutyCycle = int(speed * self.leftBias)
        self.leftMotorsPWM.ChangeDutyCycle(dutyCycle)
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*self.rightBias))

        # Left motors forward, Right motors reverse
        GPIO.output(self.leftMotorsForward, True)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, False)
        GPIO.output(self.rightMotorsReverse, True)

    # Stops all wheels
    def stop(self):
        self.leftMotorsPWM.ChangeDutyCycle(0)
        self.rightMotorsPWM.ChangeDutyCycle(0)

    # Clears all setup on pins
    def exit(self):
        self.stop()
        GPIO.cleanup()

def main(stdscr):
    # Curses setup for real-time keyboard input
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Don't block waiting for a key press
    stdscr.timeout(100) # Refresh the screen every 100ms

    # --- ⚙️ PIN CONFIGURATION ---
    # !!! IMPORTANT !!!
    # Replace these placeholder pin numbers with the actual BCM pin numbers (https://pinout.xyz)
    # you have connected to your motor driver.
    # Format: (Enable Pin, Forward Pin, Reverse Pin)
    LEFT_MOTORS = (2, 3, 4)  # Example: (EN_A, IN1, IN2)
    RIGHT_MOTORS = (22, 27, 17) # Example: (EN_B, IN3, IN4)
    
    # Initialize the robot
    robot = MotorController(leftMotors=LEFT_MOTORS, rightMotors=RIGHT_MOTORS)
    speed = 75  # Default speed (0-100)

    # Display control instructions
    stdscr.addstr(0, 0, "🤖 Robot Control Enabled")
    stdscr.addstr(2, 0, "w: Forward")
    stdscr.addstr(3, 0, "s: Reverse")
    stdscr.addstr(4, 0, "a: Turn Left")
    stdscr.addstr(5, 0, "d: Turn Right")
    stdscr.addstr(6, 0, "SPACE: Stop")
    stdscr.addstr(8, 0, "Press 'q' to quit.")
    stdscr.addstr(10, 0, "Status: Waiting for command...")
    
    action = ""

    # Main control loop
    while True:
        try:
            key = stdscr.getch() # Get user input
            stdscr.refresh()

            # Quit the program
            if key == ord('q'):
                action = "Quitting..."
                break

            # Movement Controls
            elif key == ord('w'):
                action = "Moving Forward"
                robot.moveForward(speed)
            elif key == ord('s'):
                action = "Moving Reverse"
                robot.moveReverse(speed)
            elif key == ord('a'):
                action = "Turning Left  "
                robot.turnLeft(speed)
            elif key == ord('d'):
                action = "Turning Right "
                robot.turnRight(speed)
            elif key == ord(' '):
                action = "Stopping      "
                robot.stop()
            # # If no key is pressed, the robot stops.
            # # getch() returns -1 if no key is pressed within the timeout.
            # * Uncomment the next 3 lines to make the robot stop when no keys are pressed
            # elif key == -1:
            #     action = "Stopped       "
            #     robot.stop()

            stdscr.addstr(10, 8, action)

        except (KeyboardInterrupt, SystemExit):
            break

    # Cleanup before exiting
    stdscr.addstr(10, 8, "Cleaning up and exiting...")
    stdscr.refresh()
    time.sleep(1)
    robot.exit()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except Exception as e:
        # This will run if curses fails to initialize, ensuring GPIO cleanup
        print("An error occurred. Cleaning up GPIO.")
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        print(f"Error: {e}")