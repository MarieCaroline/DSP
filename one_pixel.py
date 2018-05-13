import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack

cap = cv2.VideoCapture('output.avi')
Bvalues = []
Gvalues = []
Rvalues = []


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
    blue = frame[240, 320, 0]
    green = frame[240, 320, 1]
    red = frame[240, 320, 2]

    # put bgr values in their own lists
    Bvalues.append(blue)
    Gvalues.append(green)
    Rvalues.append(red)
    
cv2.destroyAllWindows()

# fft

f = 10 #frequency in cycles/sec
f_s = 20 # sampling rate or number of measurements per second
length = len(Bvalues)
stoptime = length/20
t = np.linspace(0, stoptime, length)

#show the output of bgr values on a plot
# plt.plot(t, Bvalues)
# plt.plot(t, Gvalues)
# plt.plot(t, Rvalues)
# plt.xlabel('time(sec)')
# plt.ylabel('BGR values')
# plt.legend(['Blue', 'Green', 'Red'])
# plt.show()


#fft p2
X = fftpack.fft(Rvalues)
freqs = fftpack.fftfreq(length)*f_s

#plt.plot(freqs, np.abs(X), '.')
#plt.plot(freqs, X, '.')
#plt.xlabel('Frequency')
#plt.ylabel('Magnitude')
#plt.xlim(0, 5)
#plt.ylim(0, 1000)
# plt.show()

#applying filter
AmplX = list(X[50:80])
AmplXX = list([i*10 for i in AmplX])
Xnew = list(X[:])
Xnew[50:80] = list(AmplXX)

#inverse fft
inverseX = fftpack.ifft(X)
inverseXnew = fftpack.ifft(Xnew)

plt.plot(t, Rvalues,'.')
plt.plot(t, inverseX, '.')
plt.plot(t, inverseXnew, '.')
plt.xlabel('time(sec)')
plt.ylabel('Red values')
plt.legend(['OriginalRed', 'Check', 'Intense'])
plt.show()

###
removed_imaginaries = np.real(inverseXnew)

integers = []

for i in removed_imaginaries:
    now_round = round(i)
    and_int = int(now_round)
    integers.append(and_int)

print integers
#applying new red values to video
cap = cv2.VideoCapture('output.avi')

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'DIVX')

out = cv2.VideoWriter('output1.avi',fourcc, 20.0, (height,width), True)
i = 0
while(cap.isOpened()):
    _, frame = cap.read()
    try:
        frame[1]
    except:
        print "blank"
        break
    # if red value greater than 255 it changes to 255
    if integers[i] > 255:
        integers[i] = 255
    frame[240, 320, 2] = integers[i]
    i += 1
    
    # write the changed
    out.write(frame)

    cv2.imshow('frame',frame)

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()







