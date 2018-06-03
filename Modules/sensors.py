import RPi.GPIO as GPIO
import time

class Ultrasonic:

	def __init__(self, ultrasonics):
		self.usTrig = []
		self.usEcho = []
		for i in range(len(ultrasonics)):
			print 'I is: ', i
			self.usTrig.append(ultrasonics[i][0])
			self.usEcho.append(ultrasonics[i][1])
			GPIO.setup(ultrasonics[i][0], GPIO.OUT)
			GPIO.setup(ultrasonics[i][1], GPIO.IN)			

	def usData(self, usID):

		GPIO.output(self.usTrig[usID], True)
		time.sleep(0.00001)
		GPIO.output(self.usTrig[usID], False)
		
		endTime = time.time()
		startTime = time.time()  #  add this new time stamp
		
		while GPIO.input(self.usEcho[usID]) == 0:
			startTime = time.time()
		while GPIO.input(self.usEcho[usID]) == 1:
			endTime = time.time()

		timeElapsed = endTime - startTime
		distance = timeElapsed * 17150
		return distance
	
	def isWall(self, usID):
		return True if self.usData(usID) < 10 or self.usData(usID) > 500 else False
