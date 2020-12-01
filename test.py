import time
import os
import io
import numpy as np
from picamera import PiCamera, mmal, mmalobj, exc
import picamera.array
from tqdm import tqdm, trange

camera = PiCamera()

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

'''# Capture image
print("Capturing image...")

stream = io.BytesIO()

start_time = time.time()

camera.capture(stream, 'jpeg', bayer=True)

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(stream.getbuffer().nbytes)'''



'''# Capture image
print("Capturing image...")

stream = picamera.array.PiBayerArray(camera)

start_time = time.time()

camera.capture(stream, 'jpeg', bayer=True)
#rawimg = (stream.demosaic() >> 2).astype(np.uint16)

execution_time = time.time() - start_time

print('Time is: ', execution_time)
print(stream.getbuffer().nbytes)'''
'''
print("Capturing image...")

stream = picamera.PiCameraCircularIO(camera, size=10237440)

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




stream = picamera.array.PiRGBArray(camera)

camera.start_preview()
camera.start_recording(fname, 'rgb')

for remaining in trange(5, 0, -1):
	camera.wait_recording(1)
camera.stop_recording()


print('done')









