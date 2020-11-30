import time
import os
import io
import numpy as np
import picamera
import picamera.array

'''
# Capture image
print("Capturing image...")

start_time = time.time()

with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        # Demosaic data and write to rawimg
        rawimg = stream.demosaic()

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(rawimg.size)
'''

# Capture image
print("Capturing image...")

start_time = time.time()

stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.capture(stream, 'jpeg', bayer=True)

execution_time = time.time() - start_time

print('Time is: ', execution_time)