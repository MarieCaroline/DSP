import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
import time

amplification = 150
#width area
start_x = 300
finish_x = 380
#height area
start_y = 155
finish_y = 190

start_freq = 40
end_freq = 65

stallTimer = 100

length_recording = 20

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('input.avi',fourcc, 20.0, (640,480))
start_time = time.time()
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        cv2.rectangle(frame,(start_x,start_y),(finish_x,finish_y),(0,0,0),3)
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    current_time = time.time()
    elapsed = current_time - start_time
    if elapsed > length_recording:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture('input.avi')
Rvalues = []
#frameNum = 0 #
while(cap.isOpened()):
    
    # Take each frame
    _, frame = cap.read()
 #   if frameNum < stallTimer: #
  #      frameNum +=1 #
   #     continue
    try:
        frame[1]
    except:
        #print "blank"
        break

    # find size
    width, height = frame.shape[:2]

    #find BGR value of one pixel
    # blue = frame[240, 320, 0]
    # green = frame[240, 320, 1]
    # red = frame[240, 320, 2]

    # find R values for a 40x40 square
    row_columns = []
    for y in range(start_y,finish_y):
        column_values = []
        for x in range(start_x,finish_x):
            red = frame[y, x, 2]
            column_values.append(red)
        row_columns.append(column_values)
    Rvalues.append(row_columns)

cv2.destroyAllWindows()


# fft setup

f = 10 #frequency in cycles/sec
f_s = 20 # sampling rate or number of measurements per second
length = len(Rvalues)
stoptime = length/20
t = np.linspace(0, stoptime, length)
freqs = fftpack.fftfreq(length)*f_s

#fft p2
heart_rates = []
highest_amplitudes = []
for y in range(len(row_columns)):
    for x in range(len(column_values)):
        fourier_list = []
        for frame in range(len(Rvalues)):
            fourier_list.append(Rvalues[frame][y][x])
        fourier_transform = fftpack.fft(fourier_list)

        #applying the filter
        points_to_increase = list(fourier_transform[start_freq:end_freq])
        highest_amplitude = max(points_to_increase)
        highest_amplitudes.append(highest_amplitude)
        if abs(highest_amplitude) > 100:
            heart_rate = (points_to_increase.index(highest_amplitude)+start_freq)
            heart_rates.append(heart_rate)
        amplified_points = list([i*amplification for i in points_to_increase])
        amplified_frequency_spectrum = list(fourier_transform)
        amplified_frequency_spectrum[start_freq:end_freq] = list(amplified_points)

        #inverse fft
        inverse_fourier = fftpack.ifft(amplified_frequency_spectrum)

        #making output usable
        removed_imaginaries = np.real(inverse_fourier)
        integers = []
        for i in removed_imaginaries:
            now_round = round(i)
            and_int = int(now_round)
            if and_int > 255:
                and_int = 255
            if and_int < 0:
                and_int = 0
            integers.append(and_int)
        for frame in range(len(Rvalues)):
            Rvalues[frame][y][x] = integers[frame]

print "Heart Reat (mean, max, min)"
print np.mean(heart_rates)
print max(heart_rates)
print min(heart_rates)
text = []
if len(heart_rates) < 300:
    text = "Not human?"
else:
    text = "%s bpm" %(int(round(np.mean(heart_rates))))

#applying new red values to video
cap = cv2.VideoCapture('input.avi')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('output4.avi',fourcc, 20.0, (height,width), True)

i = 0
#frameNum = 0 #
while(cap.isOpened()):
    _, frame = cap.read()
 #   if frameNum < stallTimer:
  #      frameNum+=1
   #     continue
    try:
        frame[1]
    except:
        #print "blank"
        break
    for y in range(start_y, finish_y):
        for x in range(start_x,finish_x):
            frame[y, x, 2] = Rvalues[i][y-start_y][x-start_x]
    i += 1
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, (400,400), font, 1, (0,0,0), 1, 1) 
    
    # write the changed
    out.write(frame)

    cv2.imshow('frame',frame)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()





