import RPi.GPIO as GPIO
import time

class RobotControl:
	# Pulses that control the motors' rotation direction as servos
	clockwisePulse = 3
	antiClockwisePulse = 11
	stopPulse = 0
	robotDirection = -1

	# Initialize the motors and create class attribute for every motor
	def __init__(self, m1, m2, m3, m4):
		GPIO.setup(m1, GPIO.OUT)
		GPIO.setup(m2, GPIO.OUT)
		GPIO.setup(m3, GPIO.OUT)
		GPIO.setup(m4, GPIO.OUT)
		print 'Done setting up pins'

		self.motor1 = GPIO.PWM(m1, 50)
		self.motor2 = GPIO.PWM(m2, 50)
		self.motor3 = GPIO.PWM(m3, 50)
		self.motor4 = GPIO.PWM(m4, 50)
		print 'Done setting up PWMs'

		self.motor1.start(0)
		self.motor2.start(0)
		self.motor3.start(0)
		self.motor4.start(0)
		print 'Started motors\' pins'

	# Motors Directions control
	# --- Clockwise
	def __m1Clockwise(self):
		self.motor1.ChangeDutyCycle(self.clockwisePulse)

	def __m2Clockwise(self):
		self.motor2.ChangeDutyCycle(self.clockwisePulse)

	def __m3Clockwise(self):
		self.motor3.ChangeDutyCycle(self.clockwisePulse)

	def __m4Clockwise(self):
		self.motor4.ChangeDutyCycle(self.clockwisePulse)
	# --- End Clockwise

	# --- Anticlockwise
	def __m1AntiClockwise(self):
		self.motor1.ChangeDutyCycle(self.antiClockwisePulse)

	def __m2AntiClockwise(self):
		self.motor2.ChangeDutyCycle(self.antiClockwisePulse)

	def __m3AntiClockwise(self):
		self.motor3.ChangeDutyCycle(self.antiClockwisePulse)

	def __m4AntiClockwise(self):
		self.motor4.ChangeDutyCycle(self.antiClockwisePulse)
	# --- End Anticlockwise

	# --- Stop
	def __m1Stop(self):
		self.motor1.ChangeDutyCycle(self.stopPulse)

	def __m2Stop(self):
		self.motor2.ChangeDutyCycle(self.stopPulse)

	def __m3Stop(self):
		self.motor3.ChangeDutyCycle(self.stopPulse)

	def __m4Stop(self):
		self.motor4.ChangeDutyCycle(self.stopPulse)
	# --- End Stop
	# End Motors Directions Control

	# Public Control
	def toFront(self):
		print 'Robot to Front'
		self.__m1Clockwise()
		self.__m2AntiClockwise()
		self.__m3AntiClockwise()
		self.__m4Clockwise()
		self.robotDirection = 1

	def toBack(self):
		print 'Robot to Back'
		self.__m1AntiClockwise()
		self.__m2Clockwise()
		self.__m3Clockwise()
		self.__m4AntiClockwise()
		self.robotDirection = 3

	def toRight(self):
		print 'Robot to Right'
		self.__m1AntiClockwise()
		self.__m2AntiClockwise()
		self.__m3Clockwise()
		self.__m4Clockwise()
		self.robotDirection = 0

	def toLeft(self):
		print 'Robot to Left'
		self.__m1Clockwise()
		self.__m2Clockwise()
		self.__m3AntiClockwise()
		self.__m4AntiClockwise()
		self.robotDirection = 2

	def to(self, x):
		print 'Robot to ', x
		if x == 0:
			self.toRight()
		elif x == 1:
			self.toFront()
		elif x == 2:
			self.toLeft()
		elif x == 3:
			self.toBack()

	def moveDir(dir, x):
		self.to(dir)
		currentDistance = distanceTravelled	# 10
		dis = currentDistance + x
		while distanceTravelled < dis:
			True
		self.stop()
		return

	def stop(self):
		self.__m1Stop()
		self.__m2Stop()
		self.__m3Stop()
		self.__m4Stop()
