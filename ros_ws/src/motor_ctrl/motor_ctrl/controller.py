import RPi.GPIO as GPIO
import rclpy
from rclpy.node import Node
from robot_interfaces.msg import Movement # Import the new message

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
        # print("Forward") # Debug

        self.leftMotorsPWM.ChangeDutyCycle(int(speed*self.leftBias))
        self.rightMotorsPWM.ChangeDutyCycle(speed)

        GPIO.output(self.leftMotorsForward, True)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, True)
        GPIO.output(self.rightMotorsReverse, False)

     # Moves all wheels in reverse
    def moveReverse(self, speed=50):
        # print("Reverse") # Debug

        self.leftMotorsPWM.ChangeDutyCycle(int(speed*self.leftBias))
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*self.rightBias))

        GPIO.output(self.leftMotorsForward, False)
        GPIO.output(self.leftMotorsReverse, True)
        GPIO.output(self.rightMotorsForward, False)
        GPIO.output(self.rightMotorsReverse, True)

    # Turns left wheels reverse, and right wheels forward
    def turnLeft(self, speed=50):
        # print("left") # Debug

        self.leftMotorsPWM.ChangeDutyCycle(int(speed*0.9*self.leftBias))
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*1.1*self.rightBias))

        GPIO.output(self.leftMotorsForward, False)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, True)
        GPIO.output(self.rightMotorsReverse, False)

    # Turns left wheels forward, and right wheels reverse
    def turnRight(self, speed=50):
        # print("right") # Debug

        self.leftMotorsPWM.ChangeDutyCycle(int(speed*self.leftBias))
        self.rightMotorsPWM.ChangeDutyCycle(int(speed*self.rightBias))

        GPIO.output(self.leftMotorsForward, True)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, False)
        GPIO.output(self.rightMotorsReverse, False)

    # Stops all wheels
    def stop(self):
        # print("Stop") # Debug
        
        self.leftMotorsPWM.ChangeDutyCycle(0)
        self.rightMotorsPWM.ChangeDutyCycle(0)

        GPIO.output(self.leftMotorsForward, True)
        GPIO.output(self.leftMotorsReverse, False)
        GPIO.output(self.rightMotorsForward, True)
        GPIO.output(self.rightMotorsReverse, False)

    # Clears all setup on pins
    def exit(self):
        GPIO.cleanup()
    
        
class MotorControlNode(Node): # MODIFY NAME
    def __init__(self):
        super().__init__("motor_controller") # MODIFY NAME
        self.motor_controller = MotorController(leftMotors=[2,3,4], rightMotors=[17,27,22]) # Example pin numbers, replace with your actual pins
        self.subscription = self.create_subscription(
            Movement,
            "robot_movement",
            self.subscription_callback,
            10
        )
        self.get_logger().info("Motor Controller Node has been started.")


    def subscription_callback(self, msg):
        if msg.command == Movement.FORWARD:
            self.motor_controller.moveForward(msg.speed)
        elif msg.command == Movement.REVERSE:
            self.motor_controller.moveReverse(msg.speed)
        elif msg.command == Movement.TURN_LEFT:
            self.motor_controller.turnLeft(msg.speed)
        elif msg.command == Movement.TURN_RIGHT:
            self.motor_controller.turnRight(msg.speed)
        elif msg.command == Movement.STOP:
            self.motor_controller.stop()
 
 
 
def main(args=None):
    rclpy.init(args=args)
    node = MotorControlNode() # MODIFY NAME
    rclpy.spin(node)
    rclpy.shutdown()
 
 
if __name__ == "__main__":
    main()
