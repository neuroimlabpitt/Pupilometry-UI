import os
from PyQt5 import QtWidgets, uic, QtCore
import sys

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

		###########################################################################################
		## Class Variables
		###########################################################################################
		self.collect_raw = False
		self.wait_for_trigger = True


		self.show()

	###############################################################################################
	## Button Click Functions
	###############################################################################################

	# For Start Preivew Button
	def StartPreview(self):
		print('Starting Preview')

	# For Stop Preivew Button
	def StopPreview(self):
		print('Stop Preview')

	# For any Framerate Radio button
	def SetFR30(self):
		print('Framerate = 30')
	def SetFR10(self):
		print('Framerate = 10')
	def SetFR5(self):
		print('Framerate = 5')

	# For any Zoom Radio button
	def SetZoom1(self):
		print('Zoom = 1')
	def SetZoom2(self):
		print('Zoom = 2')
	def SetZoom4(self):
		print('Zoom = 4')
	def SetZoom10(self):
		print('Zoom = 10')

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

	def StopRecording(self):
		print('Stopping Recording')

	###############################################################################################
	## Helper Function
	###############################################################################################



	###############################################################################################
	## To Leave Camera System
	###############################################################################################
	def LeaveWindow(self):
		app.exit()
		os.system("clear")



app = QtWidgets.QApplication(sys.argv)
window = CamUI()
app.exec_()



