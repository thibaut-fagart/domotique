#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os
from pizypwm import *

# Set Pin 11 as Output
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

while True:
	# Start PWM with 50Hz on Pin 11
	Servo = PiZyPwm(50, 11, GPIO.BOARD)							

	# Input the Direction
        print "l : left ; r : right ; m : middle ; q : quit"
	Eingabe = raw_input("Take a choice: ") 

	# Direction "Right"
	if(Eingabe == "r"):

		# Number of Steps
		Schritte = raw_input("Number of Steps: ") 
		print Schritte, "Steps to right"
	
		# Generate PWM with 10% Dutycycle (2ms)
		Servo.start(10)
		for Counter in range(int(Schritte)):
			time.sleep(0.001)
	
		# PWM stop
		Servo.stop()
		GPIO.cleanup()

	# Direction "Middle"
	elif(Eingabe == "m"):
		Servo.start(7)
		print "Middle"
		time.sleep(1) 
		Servo.stop()
		GPIO.cleanup()
	
	# Direction "Left
	elif(Eingabe == "l"):
	
		# Number of Steps
		Schritte = raw_input("Number of Steps: ") 
		print Schritte, "Steps to left"
		
		# Generate PWM with 10% Dutycycle (1ms)
		Servo.start(5)
		for Counter in range(int(Schritte)):
			time.sleep(0.001)
		
		# Stop PWM
		Servo.stop()
		GPIO.cleanup()
	
	# Quti Programm
	elif(Eingabe == "q"):
		print "Quit Programm......"
		os._exit(1)
		Servo.stop()
		GPIO.cleanup()
		
	# Error
	else:
		print "Error."
