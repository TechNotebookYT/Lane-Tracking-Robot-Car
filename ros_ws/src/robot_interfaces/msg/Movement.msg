# Constants to define the motor command
uint8 STOP=0
uint8 FORWARD=1
uint8 REVERSE=2
uint8 TURN_LEFT=3
uint8 TURN_RIGHT=4

# The desired command action
uint8 command

# The desired speed for the action (e.g., 0-100)
# This value is ignored for the STOP command.
float32 speed