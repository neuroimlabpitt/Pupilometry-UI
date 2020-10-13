import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)	# Set as internal pull up resistor input

while True:
	GPIO.wait_for_edge(32, GPIO.RISING, timeout=195)

	time.sleep(0.05) # debounce

	if GPIO.input(32) == 0:
		print("Button Pressed!!")
	else:
		time.sleep(0.195)


'''
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:

	time.sleep(1)

	if(GPIO.input(32) == 1):
		print("Button Not Pressed")
	if(GPIO.input(32) == 0):
		print("Button Pressed")
'''