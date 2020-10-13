import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# Set as internal pull up resistor input

while True:
	GPIO.wait_for_edge(40, GPIO.FALLING, timeout=195)

	time.sleep(0.05) # debounce

	if GPIO.input(40) == 0:
		print("Button Pressed!!")
	else:
		time.sleep(0.195)