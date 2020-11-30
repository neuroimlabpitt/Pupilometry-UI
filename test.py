import time
import os
import numpy as np
import picamera
import picamera.array

# Capture image
print("Capturing image...")
with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        # Demosaic data and write to rawimg
        rawimg = stream.demosaic()

print(rawimg.size)