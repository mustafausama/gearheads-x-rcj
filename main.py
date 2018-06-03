import RPi.GPIO as GPIO
import time
import thread
import Modules.dht11 as dht

# Importing all r0obot controling classes from "Modules" folder
import Modules.control as control

#Importing all robot sensors classes from "Modules" folder
import Modules.sensors as sensors

# Main Variables

GPIO.setmode (GPIO.BOARD)

"""
                   Ultrasonic 1
                        ^
           Motor 2 /----|----\ Motor 1
                   |         |
    Ultrasonic 2 <--         --> Ultrasonic 0
                   |         |
           Motor 3 \----|----/ Motor 4
                        ^
                   Ultrasonic 3
"""

# Start Pins Variables

motor1pin = 7
motor2pin = 11
motor3pin = 12
motor4pin = 13

rescueServoPin = 21

S0 = 3
S1 = 5
S2 = 8
S3 = 10
sensorOut = 19

encoderPin = 
RFreq = 0
BFreq = 0
GFreq = 0

tempratureSensor = dht.DHT11(pin = 8)

ulstrasonicList = [ [15, 16], [18, 22], [29, 31], [32, 33] ]

distanceTravelled = 0

status = 'normal'
victimType = ''
victim = ''

currentTemp0 = tempratureSensor.read()
currentTemp = currentTemp0.temprature

GPIO.setup(rescueServoPin, GPIO.OUT)
GPIO.setup(IRPin, GPIO.OUT)
rescueServo = GPIO.PWM(rescueServoPin, 50)

robot = control.RobotControl(motor1pin, motor2pin, motor3pin, motor4pin)

def checkVictims():
	# image-processing code that detects any letter and reconizes its coordinates within the image captured
	while True:
		time.sleep(1)
		results = tempratureSensor.read()
		temp = results.temprature
		if temp - currentTemp > 7:
			status = 'victim'
			victim = 'temp'
def calculateEncoderValue():
	global distanceTravelled
	while True:
		if GPIO.input(encoderPin):
			distanceTravelled += (15*((2**(0.5)) / 2)) / 90

def intersections():
	while True:
		time.sleep(1)
		if not (ultrasonic.isWall(0) and not ultrasonic.isWall(1) and ultrasonic.isWall(2) and not ultrasonic.isWall(3)) and not (not ultrasonic.isWall(0) and ultrasonic.isWall(1) and not ultrasonic.isWall(2) and ultrasonic.isWall(3)):
			type.append([0, 0, 0, 0])
			for i in range(4):
				if(i == (robot.robotDirection - 2 if robot.robotDirection - 2 >= 0 else robot.robotDirection + 2)):
					type[-1][i] = 0
					continue
				type[-1][i] = not ultrasonic.isWall(i)
			if type == [0, 0, 0, 0]:
				status = 'de'
				continue
			status = 'is'
		#'''''''''
		GPIO.output(s2, False)
		GPIO.output(s3, False)

		startTime = time.time()
		endTime = time.time()


		while GPIO.input(sensorOut) != 1:
			startTime = time.time()
		while GPIO.input(sensorOut) == 1:
			endTime = time.time()
			break

		Rfreq = endTime - startTime


		#'''''''''
		GPIO.output(s2, True)
		GPIO.output(s3, True)

		startTime = time.time()
		endTime = time.time()


		while GPIO.input(sensorOut) != 1:
			startTime = time.time()
		while GPIO.input(sensorOut) == 1:
			endTime = time.time()
			break

		Gfreq = endTime - startTime


		#'''''''''
		GPIO.output(s2, False)
		GPIO.output(s3, True)

		startTime = time.time()
		endTime = time.time()


		while GPIO.input(sensorOut) != 1:
			startTime = time.time()
		while GPIO.input(sensorOut) == 1:
			endTime = time.time()
			break

		BFreq = endTime - startTime
		
		if RFreq < 10 and GFreq < 10 and BFreq < 10:
			status = 'dead-end'

		
def main():
	global type, points, status
	if status == 'is':
		for i, v in enumerate(type[-1]):
			if v == 1:
				robot.to(i)
				type[-1][i] = 0
				status = 'normal'
				break
	
	while status != 'vm' and status != 'de' and status != 'is':
		continue
	
	if status == 'vm':
		if victm == 'front' and ultrasonic.usData(robot.robotDirection) < 10:
			robot.stop()
			if victimType == 'h':
				robot.rescue(rescueServo)
				robot.rescue(rescueServo)
			elif victimType == 's':
				robot.rescue(rescueServo)
			elif victimType == 'u':
				time.sleep(5)
				robot.to(robotDirection)

		elif victim == 'wall':
			y = 10 + ultrasonic.usData(robot.robotDirection + 1 if robot.robotDirection + 1 < 4 else robot.robotDirection - 1)
			robot.moveDir(robot.robotDirection, (3**(0.5)) * y)
			robot.stop()
			if victimType == 'h':
				robot.rescue(rescueServo)
				robot.rescue(rescueServo)
			elif victimType == 's':
				robot.rescue(rescueServo)
			elif victimType == 'u':
				time.sleep(5)
				robot.to(robotDirection)

		elif victim == 'temp':
			robot.stop()
			robot.rescue(rescueServo)
			robot.to(robotDirection)

	if status == 'is':
		main()

	# go to parent
	if points[-1][1] == points[-2][1]: # x is common
		if points[-1][0] - points[-2][0] > 0: # need to move left
			robot.moveDir(2, points[-1][0] - points[-2][0])
			type.remove(-1)
		elif points[-1][0] - points[-2][0] < 0: # need to move right
			robot.moveDir(0, points[-2][0] - points[-1][0])
			type.remove(-1)
	elif points[-1][0] == points[-2][0]: # y is common
		if points[-1][1] - points[-2][1] > 0: # need to move back
			robot.moveDir(3, points[-1][1] - points[-2][1])
			type.remove(-1)
		elif points[-1][1] - points[-2][1] < 0: # need to move front
			robot.moveDir(1, points[-2][1] - points[-1][1])
			type.remove(-1)

# Start main code
try:
	thread.start_new_thread(intersections, ())
	thread.start_new_thread(checkVictims, ())
	thread.start_new_thread(calculateEncoderValue, ())
	main()
except KeyboardInterrupt:
	GPIO.cleanup()