import time
import os
import io
import numpy as np
from picamera import PiCamera, mmal, mmalobj, exc
import picamera.array

camera = PiCamera()
camera.resolution = (10, 10)

'''
# Capture image
print("Capturing image...")

start_time = time.time()

with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        rawimg = stream.array

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(rawimg.shape)
'''

# Capture image
print("Capturing image...")

stream = io.BytesIO()

start_time = time.time()

camera.capture(stream, 'jpeg', bayer=True)

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(stream.getbuffer().nbytes)


'''
# Capture image
print("Capturing image...")

start_time = time.time()

with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        rawimg = (stream.demosaic() >> 2).astype(np.uint16)

execution_time = time.time() - start_time

print('Time is: ', execution_time)
'''


'''print("Capturing image...")

stream = picamera.PiCameraCircularIO(camera)

start_time = time.time()

camera.capture(stream, 'jpeg', bayer=True)


execution_time = time.time() - start_time

print('Time (raw) is: ', execution_time)
'''













'''# Capture image
print("Capturing image...")

start_time = time.time()

camera.capture('image.jpeg', 'jpeg', bayer=True)


execution_time = time.time() - start_time

print('Time (raw) is: ', execution_time)
'''














