import os
from PyQt5 import QtWidgets, uic, QtCore
import sys

# GLOBALS
class CTCUi(QtWidgets.QMainWindow):

	# UI Class initializer
	def __init__(self):
		super(CTCUi, self).__init__()
		uic.loadUi('UI/cam_gui.ui', self)
		self.setFixedHeight(790)
		self.setFixedHeight(470)

		self.setWindowTitle("Camera Control")



		self.show()


	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Load Schedule Page
	#######################################################################################################################################
	#######################################################################################################################################
	def LoadScheduleWindow(self):
		uic.loadUi('src/UI/CTC/ctc_schedule_import.ui', self)
		self.setWindowTitle("CTC - Load Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)


	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Edit Schedule Page
	#######################################################################################################################################
	#######################################################################################################################################
	def EditScheduleWindow(self):
		uic.loadUi('src/UI/CTC/ctc_schedule_edit.ui', self)
		self.setWindowTitle("CTC - Edit Schedule")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'ScheduleSaveButton') # Find the button
		self.button.clicked.connect(self.saveEditedSchedule)

	def saveEditedSchedule(self):
		app.exit()



	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Dispatch Train Window
	#######################################################################################################################################
	#######################################################################################################################################
	def DispatchTrainWindow(self):
		uic.loadUi('src/UI/CTC/ctc_dispatch_train.ui', self)
		self.setWindowTitle("CTC - Dispatch Train")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.returnToMainWindow)

		self.d_block_label = self.findChild(QtWidgets.QLineEdit, 'BlockInput') # Find the text input
		self.d_time_label = self.findChild(QtWidgets.QLineEdit, 'TimeInput') # Find the input

		self.d_conf_label = self.findChild(QtWidgets.QLabel, 'ConfirmationLabel') # Find the label
		self.d_speed_label = self.findChild(QtWidgets.QLabel, 'SpeedOut') # Find the label
		self.d_auth_label = self.findChild(QtWidgets.QLabel, 'AuthorityOut') # Find the label

		self.button = self.findChild(QtWidgets.QPushButton, 'DispatchButton') # Find the button
		self.button.clicked.connect(self.DispatchTrain)


	def DispatchTrain(self):
		# Error Check block value
		try:
			int(self.d_block_label.text())
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered')
			return

		# Error Check time values
		try:
			int(self.d_time_label.text()[0] + self.d_time_label.text()[1])
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		try:
			int(self.d_time_label.text()[3] + self.d_time_label.text()[4])
		except:
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return

		# Error Check for time value
		if(len(self.d_time_label.text()) != 6):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(int(self.d_time_label.text()[0] + self.d_time_label.text()[1]) not in range(1, 13)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(int(self.d_time_label.text()[3] + self.d_time_label.text()[4]) not in range(60)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time Entered')
			return
		elif(self.d_time_label.text()[5] not in ['a', 'p']):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Time of Day  Entered (a/p)')
		# Error Check for block value
		elif((int(self.d_block_label.text()) < 0) | (len(self.d_block_label.text()) == 0)):
			self.d_conf_label.setStyleSheet("color: red")
			self.d_conf_label.setText('Error: Invalid Block Entered')
			return

		# Print confirmation to screen and take actions if information valid
		else:
			self.d_conf_label.setStyleSheet("color: green")
			self.d_conf_label.setText('Train Dispatched to Block ' + self.d_block_label.text() + ' at ' + self.d_time_label.text())
			self.d_speed_label.setText('Command Speed [to Track Controller]: 40 km/hr')
			self.d_auth_label.setText('Authority [to Track Controller]: 1000 m')


		##### Send data to server #####
		##### data = "block hour minute a/p"
		send_message(RequestCode.CTC_DISPATCH_TRAIN, self.d_block_label.text() + ' ' + self.d_time_label.text()[0] + self.d_time_label.text()[1] + ' ' + self.d_time_label.text()[3] + self.d_time_label.text()[4]+ ' ' + self.d_time_label.text()[5])

		

	#######################################################################################################################################
	#######################################################################################################################################
	# Opens Map Window
	#######################################################################################################################################
	#######################################################################################################################################
	def MapWindow(self):
		global time_timr
		uic.loadUi('src/UI/CTC/ctc_view_map.ui', self)
		self.setWindowTitle("CTC - View Map")

		self.button = self.findChild(QtWidgets.QPushButton, 'BackToMainMenu') # Find the button
		self.button.clicked.connect(self.LeaveThis)

		self.d_track_label = self.findChild(QtWidgets.QLabel, 'TrackInput') # Find the label

		# Automatically refresh Map after 700ms
		time_timr = QtCore.QTimer(self)
		time_timr.timeout.connect(self.RefreshMap)
		time_timr.start(700)

		 # Find the Blocks
		self.TBlock1 = self.findChild(QtWidgets.QPushButton, 'Block1')
		self.TBlock2 = self.findChild(QtWidgets.QPushButton, 'Block2')
		self.TBlock3 = self.findChild(QtWidgets.QPushButton, 'Block3')
		self.TBlock4 = self.findChild(QtWidgets.QPushButton, 'Block4')
		self.TBlock5 = self.findChild(QtWidgets.QPushButton, 'Block5')
		self.TBlock6 = self.findChild(QtWidgets.QPushButton, 'Block6')
		self.TBlock7 = self.findChild(QtWidgets.QPushButton, 'Block7')
		self.TBlock8 = self.findChild(QtWidgets.QPushButton, 'Block8')
		self.TBlock9 = self.findChild(QtWidgets.QPushButton, 'Block9')
		self.TBlock10 = self.findChild(QtWidgets.QPushButton, 'Block10')
		self.TBlock11 = self.findChild(QtWidgets.QPushButton, 'Block11')
		self.TBlock12 = self.findChild(QtWidgets.QPushButton, 'Block12')
		self.TBlock13 = self.findChild(QtWidgets.QPushButton, 'Block13')
		self.TBlock14 = self.findChild(QtWidgets.QPushButton, 'Block14')
		self.TBlock15 = self.findChild(QtWidgets.QPushButton, 'Block15')

	def RefreshMap(self):
		# Ping server for track occupancies
		m_tuple_data = send_message(RequestCode.CTC_SEND_GUI_OCCUPANCIES)

		# Extract string data from tuple
		m_data = m_tuple_data[1]

		for i in range(len(m_data)):
			if(m_data[i] == 't'):
				try:
					eval('self.TBlock%s.setStyleSheet(\"background-color: rgb(255, 255, 10);\")' % str(i + 1))		# if occupied change block color to yellow
					self.d_track_label.setText('Track Occupancy [from Track Controller]: Track ' + str(i + 1) + ' Occupied')
				except:
					print('Warning: Screen has been closed before  button could update')
			else:
				try:
					eval('self.TBlock%s.setStyleSheet(\"background-color: rgb(33, 255, 128);\")' % str(i + 1))		# if not occupied, change block color to green
				except:
					print('Warning: Screen has been closed before  button could update')

	def LeaveThis(self):
		global time_timr
		time_timr.stop()
		self.returnToMainWindow()


	#######################################################################################################################################
	#######################################################################################################################################
	# Return to main window from all windows function
	#######################################################################################################################################
	#######################################################################################################################################
	def returnToMainWindow(self):
		uic.loadUi('src/UI/CTC/ctc_main.ui', self)
		self.setWindowTitle("CTC Main Page")

		# In Main Window
		self.button = self.findChild(QtWidgets.QPushButton, 'LoadSchedule') # Find the button
		self.button.clicked.connect(self.LoadScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'EditSchedule') # Find the button
		self.button.clicked.connect(self.EditScheduleWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Exit') # Find the button
		self.button.clicked.connect(self.ExitModule)
		self.button = self.findChild(QtWidgets.QPushButton, 'Dispatch') # Find the button
		self.button.clicked.connect(self.DispatchTrainWindow)
		self.button = self.findChild(QtWidgets.QPushButton, 'Map') # Find the button
		self.button.clicked.connect(self.MapWindow)

		self.checkbox = self.findChild(QtWidgets.QCheckBox, 'AutomaticToggle') # Find the check box
		self.checkbox.clicked.connect(self.ToggleAutomaicMode)

		self.tplabel = self.findChild(QtWidgets.QLabel, 'ThroughputValue') # Find the label


	#######################################################################################################################################
	#######################################################################################################################################
	# Toggle for Automatic Mode
	#######################################################################################################################################
	#######################################################################################################################################
	def ToggleAutomaicMode(self):
		return None

	#######################################################################################################################################
	#######################################################################################################################################
	# Exits the Module
	#######################################################################################################################################
	#######################################################################################################################################
	def ExitModule(self):
		if(sys.platform == 'darwin'):
			os.system('python3 src/UI/login_gui.py &')
		else:
			os.system('start /B python src/UI/login_gui.py')
		app.exit()


app = QtWidgets.QApplication(sys.argv)
window = CTCUi()
app.exec_()



