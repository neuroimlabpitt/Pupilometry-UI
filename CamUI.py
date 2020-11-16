import os
from PyQt5 import QtWidgets, uic, QtCore
import sys

from picamera import PiCamera, mmal, mmalobj, exc
import RPi.GPIO as GPIO

import os, datetime, time, itertools

from tqdm import tqdm, trange
import simplejson as json

#from brightpi import *

# Define the Trigger pin
TRIGGER_PIN = 32

# GLOBALS
class CamUI(QtWidgets.QMainWindow):

	# UI Class initializer / LOAD THE UI
	def __init__(self):
		super(CamUI, self).__init__()
		uic.loadUi('UI/cam_gui.ui', self)

		# Initiaize Some Parameters
		#self.setFixedWidth(790)
		#self.setFixedHeight(470)
		self.SetFR30()
		self.SetZoom1()
		self.SetComp()

		self.setWindowTitle("Camera Control")

		###########################################################################################
		## Buttons / Screen Items
		###########################################################################################
		self.exit_button = self.findChild(QtWidgets.QPushButton, 'Exit')
		self.exit_button.clicked.connect(self.LeaveWindow)

		self.start_prev = self.findChild(QtWidgets.QPushButton, 'StartPrev')
		self.start_prev.clicked.connect(self.StartPreview)
		self.stop_prev = self.findChild(QtWidgets.QPushButton, 'StopPrev')
		self.stop_prev.clicked.connect(self.StopPreview)

		self.start_rec = self.findChild(QtWidgets.QPushButton, 'StartRec')
		self.start_rec.clicked.connect(self.StartRecording)
		self.stop_rec = self.findChild(QtWidgets.QPushButton, 'StopRec')
		self.stop_rec.clicked.connect(self.StopRecording)

		self.length_text = self.findChild(QtWidgets.QLineEdit, 'RecordingTime')
		self.fname_text = self.findChild(QtWidgets.QLineEdit, 'FName')
		self.exposure_text = self.findChild(QtWidgets.QLineEdit, 'Exposure')

		self.fr_30_radio = self.findChild(QtWidgets.QRadioButton, 'FR30')
		self.fr_30_radio.clicked.connect(self.SetFR30)
		self.fr_10_radio = self.findChild(QtWidgets.QRadioButton, 'FR10')
		self.fr_10_radio.clicked.connect(self.SetFR10)
		self.fr_5_radio = self.findChild(QtWidgets.QRadioButton, 'FR5')
		self.fr_5_radio.clicked.connect(self.SetFR5)

		self.zoom_1_radio = self.findChild(QtWidgets.QRadioButton, 'ZOOM1x')
		self.zoom_1_radio.clicked.connect(self.SetZoom1)
		self.zoom_2_radio = self.findChild(QtWidgets.QRadioButton, 'ZOOM2x')
		self.zoom_2_radio.clicked.connect(self.SetZoom2)
		self.zoom_4_radio = self.findChild(QtWidgets.QRadioButton, 'ZOOM4x')
		self.zoom_4_radio.clicked.connect(self.SetZoom4)
		self.zoom_10_radio = self.findChild(QtWidgets.QRadioButton, 'ZOOM10x')
		self.zoom_10_radio.clicked.connect(self.SetZoom10)

		self.comp_radio = self.findChild(QtWidgets.QRadioButton, 'CompRadio')
		self.comp_radio.clicked.connect(self.SetComp)
		self.raw_radio = self.findChild(QtWidgets.QRadioButton, 'RawRadio')
		self.raw_radio.clicked.connect(self.SetRaw)

		self.external_trigger_check = self.findChild(QtWidgets.QCheckBox, 'TriggerCheck')
		self.external_trigger_check.clicked.connect(self.ExternalTriggerCheck)

		self.progress_bar = self.findChild(QtWidgets.QProgressBar, 'AcquireProgress')

		###########################################################################################
		## Class Variables
		###########################################################################################
		self.collect_raw = False
		self.wait_for_trigger = False
		self.acq_num = 1
		self.trigger_pin = 32


		self.show()

	###############################################################################################
	## Button Click Functions
	###############################################################################################

	# For Start Preivew Button
	def StartPreview(self):
		print('Starting Preview')
		# Set the exposure mode to auto
		camera.exposure_mode = 'auto'

		# Start preview of camera
		camera.start_preview()

	# For Stop Preivew Button
	def StopPreview(self):
		print('Stop Preview')
		camera.stop_preview()

	# For any Framerate Radio button
	def SetFR30(self):
		print('Framerate = 30')
		camera.framerate = 30
	def SetFR10(self):
		print('Framerate = 10')
		camera.framerate = 10
	def SetFR5(self):
		print('Framerate = 5')
		camera.framerate = 5

	# For any Zoom Radio button
	def SetZoom1(self):
		print('Zoom = 1')
		camera.zoom = (0.0, 0.0, 1.0, 1.0)
	def SetZoom2(self):
		print('Zoom = 2')
		camera.zoom = (0.25, 0.25, 0.5, 0.5)
	def SetZoom4(self):
		print('Zoom = 4')
		camera.zoom = (0.375, 0.375, 0.25, 0.25)
	def SetZoom10(self):
		print('Zoom = 10')
		camera.zoom = (0.45, 0.45, 0.1, 0.1)

	# For any Comp. Radio button
	def SetComp(self):
		self.collect_raw = False
		print('Collecting Raw = ', self.collect_raw)
	def SetRaw(self):
		self.collect_raw = True
		print('Collecting Raw', self.collect_raw)

	# For External Trigger button
	def ExternalTriggerCheck(self):
		if(self.external_trigger_check.isChecked()):
			self.wait_for_trigger = True
		else:
			self.wait_for_trigger = False
		print("Wait for Trigger: ", self.wait_for_trigger)

	# For Starting the Recording
	def StartRecording(self):
		print('')
		print(self.length_text.text())
		print(self.fname_text.text())
		print(self.exposure_text.text())
		print('')
		"""Start recording or wait for trigger"""

		# Lock the gain so that it does not change
		camera.exposure_mode = 'off'

		# Check trigger state
		if self.wait_for_trigger:
			self.WaitForTrigger()

		fname = self.fname_text.text()

		if (fname == './') & (self.wait_for_trigger == False):
			date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
			fname = './' + date
		elif (fname == '') & (self.wait_for_trigger == True):
			date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
			fname = "./" + date

		if (fname[-5:] != ".h264") & (self.collect_raw == False):
			fname = fname + ".h264"
		elif (fname[-5:] != ".data") & (self.collect_raw == True):
			fname = fname + ".data"


		# Update displayed file name
		self.fname_text.setText(fname)

		# Check file doesn't exist
		if os.path.isfile(fname):
			# Warn user and do nothing
			print('File already exists!')
			return

		# Get recording time
		time_rec = int(self.length_text.text())

		# Start recording and tell user
		if self.collect_raw == True:
			camera.start_recording(fname, 'yuv')
		else:
			camera.start_recording(fname)
		print('Recording started')

		# Increase counter
		self.acq_num += 1

		# Do timed recording, if necessary
		if (time_rec > 0):
			for remaining in trange(time_rec, 0, -1):
				camera.wait_recording(1)
				self.progress_bar.setValue(int((time_rec - remaining)/time_rec))	# Update Progress level
			self.StopRecording()
		else:
			self.progress_bar.setValue(50)		# Set Progress at 50

	def StopRecording(self):
		print('Stopping Recording')
		"""Stop current recording"""
		camera.stop_recording()
		self.progress_bar.setValue(0)	# Update Progress level
		print('File saved to ', self.fname_text.text())
		self.SaveCameraParams()
		self.fname_text.setText('./')

	###############################################################################################
	## Helper Function
	###############################################################################################
	def SaveCameraParams(self):
		"""Save camera parameters to file"""
		params = {
			"analog_gain" : float(camera.analog_gain),
			"awb_gains" : [float(x) for x in camera.awb_gains],
			"awb_mode" : camera.awb_mode,
			"brightness" : camera.brightness,
			"contrast" : float(camera.contrast),
			"crop" : camera.crop,
			"digital_gain" : float(camera.digital_gain),
			"drc_strength" : camera.drc_strength,
			"exposure" : {
			"compensation" : camera.exposure_compensation,
				"mode" : camera.exposure_mode,
				"speed" : camera.exposure_speed
			},
			"flash_mode" : camera.flash_mode,
			"framerate" : float(camera.framerate),
			"hflip" : camera.hflip,
			"image_denoise" : camera.image_denoise,
			"image_effect" : camera.image_effect,
			"image_effect_params" : camera.image_effect_params,
			"iso" : camera.iso,
			"meter_mode" : camera.meter_mode,
			"resolution" : {
				"width" : camera.resolution.width,
				"height" : camera.resolution.height
			},
			"rotation" : camera.rotation,
			"sensor_mode" : camera.sensor_mode,
			"sharpness" : camera.sharpness
		}

		fname = self.fname_text.text()
		if(fname[-5:] == '.h264'):
			fname = fname.replace('.h264', '.json')
		else:
			fname = fname.replace('.data', '.json')

		with open(fname, 'w') as outfile:
			json.dump(params, outfile)

	def WaitForTrigger(self):
		'''Wait for a trigger to arrive'''

		print("Waiting for Trigger...")

		while True:
			GPIO.wait_for_edge(TRIGGER_PIN, GPIO.RISING, timeout=195)
			time.sleep(0.002) #debounce 2ms
			if GPIO.input(32) == 1:
				print("Button Pressed!!")
				print("Trigger Recived")
				break

	###############################################################################################
	## To Leave Camera System
	###############################################################################################
	def LeaveWindow(self):
		app.exit()
		os.system("clear")


'''
	# MAIN
'''
''' DISABLE BRIGHT PI
try:
	brightPi = BrightPi()
	brightPi.reset()

	# Define LEDs
	LED_ALL = (1,2,3,4,5,6,7,8)
	LED_WHITE = LED_ALL[0:4]
	LED_IR = LED_ALL[4:8]
	ON = 1
	OFF = 0
except:
	print('No BrightPi detected. Disabling LED control.')
'''

# Set up trigger input GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIGGER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # internal pull down

# Camera Set Up
# Create camera object with defined settings
camera = PiCamera()
camera.rotation = 180
camera.color_effects = (128,128) #b/w
camera.framerate = 30
camera.preview_fullscreen = False
camera.sensor_mode = 1

# User Added Camera settings
camera.shutter_speed = 60000


#calculate preview size
height = int(320 * 0.75)
width = int(320)
camera.preview_window = (100, 20, width, height)

# UI Setup
app = QtWidgets.QApplication(sys.argv)
window = CamUI()
app.exec_()



