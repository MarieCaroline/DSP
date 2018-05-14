import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

cap = cv2.VideoCapture('recorded.avi')
Rvalues = []

amplification = 150
#width area
start_x = 300
finish_x = 380
#height area
start_y = 155
finish_y = 190

start_freq = 22
end_freq = 40

while(cap.isOpened()):

    # Take each frame
    _, frame = cap.read()
    try:
        frame[1]
    except:
        print "blank"
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
for y in range(len(row_columns)):
    for x in range(len(column_values)):
        fourier_list = []
        for frame in range(len(Rvalues)):
            fourier_list.append(Rvalues[frame][y][x])
        fourier_transform = fftpack.fft(fourier_list)

        #applying the filter
        points_to_increase = list(fourier_transform[start_freq:end_freq])
        highest_amplitude = max(points_to_increase)
        heart_rate = 2*(points_to_increase.index(highest_amplitude)+start_freq)
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

#applying new red values to video
cap = cv2.VideoCapture('recorded.avi')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
out = cv2.VideoWriter('recorded_output.avi',fourcc, 20.0, (height,width), True)

i = 0
while(cap.isOpened()):
    _, frame = cap.read()
    try:
        frame[1]
    except:
        print "blank"
        break
    for y in range(start_y, finish_y):
        for x in range(start_x,finish_x):
            frame[y, x, 2] = Rvalues[i][y-start_y][x-start_x]
    i += 1
    
    # write the changed
    out.write(frame)

    cv2.imshow('frame',frame)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

print np.mean(heart_rates)




