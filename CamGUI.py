#!/usr/bin/env python

try:
    from Tkinter import *
    from tkFileDialog import asksaveasfilename
except:
    from tkinter import *
    from tkinter.filedialog import asksaveasfilename

import sys
from picamera import PiCamera, mmal, mmalobj, exc
import RPi.GPIO as GPIO
#from brightpi import *

import os, datetime, time, itertools

from tqdm import tqdm, trange
import simplejson as json

# Parser for optional arguments
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fullscreen', action='store_true', default=False,
    dest='fullscreen', help="Toggle fullscreen preview.")
parser.add_argument("--trigger_pin",  type=int, default=32,
    help="Raspberry's trigger input pin as specified with 'GPIO.board'.",)
parser.add_argument("--light_off", action='store_true', default=False,
    dest='light_off', help="Disable BrightPi.")
parser.add_argument("--prevsize",  type=float, default=320,
    help="Width of the preview window.",)
parser.add_argument("-r", "--framerate",  type=int, default=30,
    help="Camera frame rate used for recordings.",)
parser.add_argument("--rotation",  type=int, default=180,
    help="Rotation of camera output picture, in degree.",)
parser.add_argument("--timeout",  type=int, default=20,
    help="How long the program will wait for an external trigger.",)
parser.add_argument("--sensor_mode",  type=int, default=1,
    help="Which sensor mode (1-7) should be used.",)
args = parser.parse_args()

effects = ['off', 'all', 'IR', 'white']
zooms = ['1x', '2x', '4x', '10x']
framerates = ['30', '10', '5']
datatype = ['compressed', 'raw']

class CamGUI:
    """A simple GUI to control RasPi camera recordings

    This simple GUI lets users start and stop camera preview and recording,
    as well as control a BrightPi light source. Length and storage path can be
    set. The GUI accepts external triggers on GPIO21, pull LOW to trigger.
    """

    def __init__(self, master):
        """Create and pack all GUI elements"""

        self.raw_collection = False

        self.master = master
        master.title("Camera Control")

        self.label = Label(master, text="Control the camera!")
        self.label.pack()

        self.open_preview = Button(master, text="Start Preview",
            command=self.start_prev)
        self.open_preview.pack(side=LEFT)

        self.close_preview = Button(master, text="Stop Preview",
            command=camera.stop_preview)
        self.close_preview.pack(side=RIGHT)

        self.record_time_label = Label(master, text="Time (s)")
        self.record_time_label.pack()

        self.record_time_value = Entry(master)
        self.record_time_value.insert(0, "0")
        self.tooltip = Label(master, text="", width=40)
        self.record_time_value.pack()
        self.tooltip.pack(fill = "x")

        self.record_time_value.bind("<Enter>", self.on_enter)
        self.record_time_value.bind("<Leave>", self.on_leave)

        self.file_name_label = Label(master, text="File name")
        self.file_name_label.pack()

        self.file_name_value = Entry(master)
        self.file_name_value.insert(0, "")
        self.file_name_value.pack()

        self.save_file = Button(master, text="Browse...",
            command=self.point_save_location)
        self.save_file.pack()
        self.wait_trigger_flag = IntVar()
        self.wait_trigger = Checkbutton(master, text="External trigger",
            variable=self.wait_trigger_flag)
        self.wait_trigger.pack()

        self.start_rec = Button(master, text="Start Recording",
            command=self.start_recording)
        self.start_rec.pack()

        self.stop_rec = Button(master, text="Stop Recording",
            command=self.stop_recording)
        self.stop_rec.pack()

        # Zoom control
        self.zoom_label = Label(master, text="Set zoom")
        self.zoom_label.pack(side=LEFT)

        ZOOM_Var = StringVar(root)
        ZOOM_Var.set(zooms[0])
        self.zoom_option = OptionMenu(master, ZOOM_Var, *zooms,
            command=self.set_zoom)
        self.zoom_option.pack(side=LEFT)

        # raw control
        self.zoom_label = Label(master, text="Set Raw collection")
        self.zoom_label.pack(side=RIGHT)
        RAW_Var = StringVar(root)
        RAW_Var.set(datatype[0])
        self.zoom_option = OptionMenu(master, RAW_Var, *datatype,
            command=self.set_datatype)
        self.zoom_option.pack(side=RIGHT)

        # Framerate control
        self.framerate_label = Label(master, text="Set Framerate")
        self.framerate_label.pack()

        FR_Var = StringVar(root)
        FR_Var.set(framerates[0])
        self.framerate_option = OptionMenu(master, FR_Var, *framerates,
            command=self.set_framerate)
        self.framerate_option.pack(side=RIGHT)

        # Exposure control
        self.exposure_label = Label(master, text="Exposure Time")
        self.exposure_label.pack()

        self.exposure_value = Entry(master)
        self.exposure_value.insert(0, "0")
        self.exposure_value.pack()

        self.exposure_set = Button(master, text="Set",
            command=self.set_exposure_time(self.exposure_value.get()))
        self.exposure_set.pack()

        # Initialise acquisition counter
        self.acq_num = 1;

        # Skip lamp control, if necessary
        if not args.light_off:
            self.light_label = Label(master, text="LED control")
            self.light_label.pack()

            LIGHT_Var = StringVar(root)
            LIGHT_Var.set(effects[0])
            self.light_Option = OptionMenu(master, LIGHT_Var, *effects,
                command=self.set_light)
            self.light_Option.pack()


    def on_enter(self, event):
        """Tooltip for record time label"""

        self.tooltip.configure(text="Use 0 for infinite recording.")

    def on_leave(self, event):
        """Tooltip for record time label"""

        self.tooltip.configure(text="")

    def save_camera_params(self):
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

        fname = self.file_name_value.get()
        fname = fname.replace('.h264', '.json')

        with open(fname, 'w') as outfile:
            json.dump(params, outfile)

    def set_light(self, value):
        """BrightPi control"""

        if (value == 'all'):
            leds_on = LED_ALL
            leds_off = 0
        elif (value == 'IR'):
            leds_on = LED_IR
            leds_off = LED_WHITE
        elif (value == 'white'):
            leds_on = LED_WHITE
            leds_off = LED_IR
        else:
            leds_on = 0
            leds_off = LED_ALL

        if not (leds_off == LED_ALL):
            brightPi.set_led_on_off(leds_on, ON)

        if not (leds_on == LED_ALL):
            brightPi.set_led_on_off(leds_off, OFF)

    def set_zoom(self, value):
        """Zoom control"""

        if (value == '2x'):
            zoom = (0.25, 0.25, 0.5, 0.5)
        elif (value == '4x'):
            zoom = (0.375, 0.375, 0.25, 0.25)
        elif (value == '10x'):
            zoom = (0.45, 0.45, 0.1, 0.1)
        else:
            zoom = (0.0, 0.0, 1.0, 1.0)

        camera.zoom = zoom

    def set_datatype(self, value):
        """Raw Flag"""

        if (value == 'raw'):
            self.raw_collection = True		# Set the raw flag to 1
            print('Data Collection Raw')
        else:
        	self.raw_collection = False

    def set_framerate(self, value):
        """Framerate control"""

        if(value == '5'):
            rate = 5
            print('Framerate = 5')
        elif(value == '10'):
            rate = 10
            print('Framerate = 10')
        else:
            rate = 30
            print('Framerate = 30')

        # Set Framerate
        camera.framerate = rate

    def set_exposure_time(self, value):
        """Exposure control"""

        try:
            value = int(value)
        except:
            print("INVALID exposure time (NaN entered) ... Setting to auto")
            shut_speed = 0

        fps = camera.framerate

        # make sure value isnt greater than 1/fps
        if value > 1/fps:
            print("INVALID exposure time (greater than 1/fps) ... Setting to max allowable")
            shut_speed = 1/fps
        elif value < 10000:
            print("INVALID exposure time (too low) ... Setting to auto")
            shut_speed = 0
        else:
            shut_speed = value
            print("shut_speed = ", value, "muS")

        # Set Shutter Speed
        camera.shutter_speed = shut_speed

    def start_prev(self):
    	# Set the exposure mode to auto
        camera.exposure_mode = 'auto'

        # Start preview of camera
        camera.start_preview()

    def start_recording(self):
        """Start recording or wait for trigger"""

        # Lock the gain so that it does not change
        camera.exposure_mode = 'off'

        # Check trigger state
        doWait = self.wait_trigger_flag.get()
        if doWait:
            self.wait_for_trigger()

        fname = self.file_name_value.get()

        if (fname == "") & (self.raw_collection == False):
            date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            fname = "" + date
        elif (fname == "./") & (self.raw_collection == True):
            date = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            fname = "./" + date

        if (fname[-5:] != ".h264") & (self.raw_collection == False):
            fname = fname + ".h264"
        elif (fname[-5:] != ".data") & (self.raw_collection == True):
            fname = fname + ".data"

        # Update displayed file name
        self.file_name_value.delete(0,END)
        self.file_name_value.insert(0, fname)

        # Add counter to filename (without updating dispalay)
        filename, file_extension = os.path.splitext(fname)
        filename = filename + str(self.acq_num).zfill(3)
        fname = filename+file_extension

        # Check file doesn't exist
        if os.path.isfile(fname):
            # Warn user and do nothing
            sys.stdout.write("\nFile already exists!\n")
            return

        # Get recording time
        time_rec = int(self.record_time_value.get())

        print('raw_collection = ', self.raw_collection)

        # Start recording and tell user
        if self.raw_collection == True:
        	camera.start_recording(fname, 'yuv')
        else:
        	camera.start_recording(fname)
        sys.stdout.write("\rRecording started\n")

        # Increase counter
        self.acq_num += 1

        # Do timed recording, if necessary
        if (time_rec > 0):
            for remaining in trange(time_rec, 0, -1):
                camera.wait_recording(1)

            self.stop_recording()

    def stop_recording(self):
        """Stop current recording"""

        camera.stop_recording()
        sys.stdout.write("File saved to {:s}\n".format(self.file_name_value.get()))
        self.file_name_value.insert(0, "")
        #self.save_camera_params()

    def point_save_location(self):
        """ Ask user where to save the file"""

        fname = asksaveasfilename(
            defaultextension=".h264",
            initialdir="./")

        if fname is None:
            return

        self.file_name_value.delete(0,END)
        self.file_name_value.insert(0,fname)

    def wait_for_trigger(self):
        """Wait for a trigger to arrive

        When waiting for a trigger, the timeout value in GPIO.wait_for_edge()
        defines maximum response latency. Length of range in for loop multiplied
        by timeout + debounce time gives time until trigger timeout."""

        print("Waiting for Trigger...")

        while True:
            GPIO.wait_for_edge(args.trigger_pin, GPIO.RISING, timeout=195)
            time.sleep(0.002) #debounce 2ms
            if GPIO.input(32) == 1:
                print("Button Pressed!!")
                print("Trigger Recived")
                break

# Set up trigger input GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(args.trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # internal pull down

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
    sys.stdout.write("\nNo BrightPi detected. Disabling LED control.\n")

    # Disable LED option menu
    args.light_off = True

# Create camera object with defined settings
camera = PiCamera()
camera.rotation = args.rotation
camera.color_effects = (128,128) #b/w
camera.framerate = args.framerate
camera.preview_fullscreen = args.fullscreen
camera.sensor_mode = args.sensor_mode

# User Added Camera settings
camera.shutter_speed = 60000


#calculate preview size
height = int(args.prevsize * 0.75)
width = int(args.prevsize)
camera.preview_window = (100,20,width,height)

# Create GUI
root = Tk()
my_gui = CamGUI(root)

# Loop until interrupted
try:
    root.mainloop()
except KeyboardInterrupt:
    GPIO.cleanup()
    camera.close

    try:
        brightPi.reset()
    except:
        pass

