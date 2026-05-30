import cv2
import numpy as np

cap = cv2.VideoCapture('chromatic.mp4')
success, frame = cap.read()

red_values = []
count = 0

while success:
    if count % 30 == 0:
        b, g, r = cv2.split(frame)
        red_values.append(int(r[0, 0])) # Assuming solid color frame
    success, frame = cap.read()
    count += 1
cap.release()

print(''.join([chr(v) for v in red_values]))
