from gpiozero import Motor

class MotorController():
    """
    MOTOR CONTROL
    --
    This method contains functions to move the car in different directions
    """

    # Initialize Pin Setup
    def __init__(self, leftMotors, rightMotors, leftBias=1, rightBias=1):
        # leftMotors and rightMotors are tuples: (forward_pin, reverse_pin)
        self.leftMotor = Motor(forward=leftMotors[1], backward=leftMotors[2])
        self.rightMotor = Motor(forward=rightMotors[1], backward=rightMotors[2])

        self.leftBias = leftBias
        self.rightBias = rightBias

    # Moves all wheels forward
    def moveForward(self, speed=50):
        # print("Forward") # Debug
        left_power = speed / 100.0 * self.leftBias
        right_power = speed / 100.0 * self.rightBias
        self.leftMotor.forward(speed=left_power)
        self.rightMotor.forward(speed=right_power)

     # Moves all wheels in reverse
    def moveReverse(self, speed=50):
        # print("Reverse") # Debug
        left_power = speed / 100.0 * self.leftBias
        right_power = speed / 100.0 * self.rightBias
        self.leftMotor.backward(speed=left_power)
        self.rightMotor.backward(speed=right_power)

    # Steers the car based on a turn value
    def steer(self, speed=40, turn=0):
        """
        Moves the car forward, adjusting wheel speeds for turning.
        :param speed: The base speed of the car (0-100, converted to 0-1 for gpiozero).
        :param turn: The turning value (-100 to 100, converted to 0-1 for gpiozero).
                     Positive values turn right, negative values turn left.
        """
        leftSpeed = speed + turn
        rightSpeed = speed - turn

        # Clamp speeds to be within 0-100 range
        leftSpeed = max(0, min(100, leftSpeed))
        rightSpeed = max(0, min(100, rightSpeed))

        # Convert to 0-1 range for gpiozero
        left_power = leftSpeed / 100.0 * self.leftBias
        right_power = rightSpeed / 100.0 * self.rightBias

        # Apply power to motors
        # Assuming positive speed means forward
        self.leftMotor.forward(speed=left_power)
        self.rightMotor.forward(speed=right_power)

    # Turns left wheels reverse, and right wheels forward
    def turnLeft(self, speed=50):
        # print("left") # Debug
        # This method might need re-evaluation with the new steer method
        # For now, a simple implementation: left motor stops, right motor goes forward
        self.leftMotor.stop()
        self.rightMotor.forward(speed=speed / 100.0 * self.rightBias)

    # Turns left wheels forward, and right wheels reverse
    def turnRight(self, speed=50):
        # print("right") # Debug
        # This method might need re-evaluation with the new steer method
        # For now, a simple implementation: right motor stops, left motor goes forward
        self.leftMotor.forward(speed=speed / 100.0 * self.leftBias)
        self.rightMotor.stop()

    # Stops all wheels
    def stop(self):
        # print("Stop") # Debug
        self.leftMotor.stop()
        self.rightMotor.stop()

    # Clears all setup on pins
    def exit(self):
        # gpiozero handles cleanup automatically on program exit,
        # but explicitly closing motors is good practice.
        self.leftMotor.close()
        self.rightMotor.close()
