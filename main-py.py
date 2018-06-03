import RPi.GPIO as GPIO
import time
import thread
import Modules.dht11 as dht

# Importing all robot controling classes from "Modules" folder
import Modules.control as control

#Importing all robot sensors classes from "Modules" folder
import Modules.sensors as sensors

GPIO.setmode(GPIO.BOARD)

motor1pin = 7
motor2pin = 11
motor3pin = 12
motor4pin = 13


encoderPin = 8
tempratureSensor = dht.DHT11(pin = 24)
ulstrasonicList = [ [15, 16], [18, 22], [29, 31], [32, 33] ]

points = []
type = []
distanceTravelled = 0

currentTemp0 = tempratureSensor.read()
currentTemp = currentTemp0.temperature

GPIO.setup(encoderPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

robot = control.RobotControl(motor1pin, motor2pin, motor3pin, motor4pin)
ultrasonic = sensors.Ultrasonic(ulstrasonicList)

def encoder():
	global distanceTravelled
	prev_input = 0
	total = 0
	while True:
		input = GPIO.input(encoderPin)
		if ((not prev_input) and input):
			total = total + 1
		prev_input = input
		distanceTravelled += (32 * ( (2**(0.5)) / 2) ) / 90

def parent():
	global distanceTravelled
	if points[-1][1] == points[-2][1]: # x is common
		if points[-1][0] - points[-2][0] > 0: # need to move left
			robot.to(2)
			while not ultrasonic.isWall(2):
				continue
			type.remove(-1)
		elif points[-1][0] - points[-2][0] < 0: # need to move right
			robot.to(0)
			while not ultrasonic.isWall(0):
				continue
			type.remove(-1)
	elif points[-1][0] == points[-2][0]: # y is common
		if points[-1][1] - points[-2][1] > 0: # need to move back
			robot.to(3)
			while not ultrasonic.isWall(3):
				continue
			type.remove(-1)
		elif points[-1][1] - points[-2][1] < 0: # need to move front
			robot.to(1)
			while not ultrasonic.isWall(1):
				continue
			type.remove(-1)
def main():
	global distanceTravelled
	if not (ultrasonic.isWall(0) and not ultrasonic.isWall(1) and ultrasonic.isWall(2) and not ultrasonic.isWall(3)) and not (not ultrasonic.isWall(0) and ultrasonic.isWall(1) and not ultrasonic.isWall(2) and ultrasonic.isWall(3)):
		time.sleep(0.2)
		robot.stop()
		type.append([0, 0, 0, 0])
		points.append([points[-1][0], points[-1][1]])
		if (robot.robotDirection == 0):
			points[-1][0] = points[-1][0] + distanceTravelled
		elif (robot.robotDirection == 1):
			points[-1][1] = points[-1][1] + distanceTravelled
		elif (robot.robotDirection == 2):
			points[-1][0] = points[-1][0] - distanceTravelled
		elif (robot.robotDirection == 3):
			points[-1][1] = points[-1][1] - distanceTravelled
		distanceTravelled = 0
	for i in range(4):
		if(i == (robot.robotDirection - 2 if robot.robotDirection - 2 >= 0 else robot.robotDirection + 2)):
			type[-1][i] = 0
			continue
		type[-1][i] = not ultrasonic.isWall(i)

	for i, v in enumerate(type[-1]):
		if v == 1:
			robot.to(i)
			type[-1][i] = 0
			break

	while not ultrasonic.isWall(robot.robotDirection):
		results = tempratureSensor.read()
		temp = results.temperature
		if temp - currentTemp > 5:
			robot.stop()
			time.sleep(5)
			robot.to(robot.robotDirection)

	if not (ultrasonic.isWall(0) and not ultrasonic.isWall(1) and ultrasonic.isWall(2) and not ultrasonic.isWall(3)) and not (not ultrasonic.isWall(0) and ultrasonic.isWall(1) and not ultrasonic.isWall(2) and ultrasonic.isWall(3)):
		main()
	
	parent()

	while(type[-1][0] == 1 or type[-1][1] == 1 or type[-1][2] == 1 or type[-1][3] == 1):
		main()
	
try:
	thread.start_new_thread(encoder, ())
	robot.to(1)
	points.append([0, 0])
	main()
	GPIO.cleanup()
except KeyboardInterrupt:
	GPIO.cleanup()