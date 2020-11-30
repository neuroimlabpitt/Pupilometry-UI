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
        rawimg = stream.array

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(rawimg.shape)
'''
'''
# Capture image
print("Capturing image...")

start_time = time.time()

stream = io.BytesIO()

with picamera.PiCamera() as camera:
    camera.capture(stream, 'jpeg', bayer=True)

execution_time = time.time() - start_time

print('Time is: ', execution_time)
'''

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

# Capture image
print("Capturing image...")

start_time = time.time()

with picamera.PiCamera() as camera:
    picamera.PiCamera().camera.capture('image.jpeg', 'jpeg', bayer=True)


execution_time = time.time() - start_time

print('Time (raw) is: ', execution_time)



print("Capturing image...")

start_time = time.time()

with picamera.PiCamera() as camera:
    picamera.PiCamera().camera.capture('image.jpeg', 'jpeg')


execution_time = time.time() - start_time

print('Time is: ', execution_time)














