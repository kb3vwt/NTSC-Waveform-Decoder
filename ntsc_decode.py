#!/usr/bin/python
from DS1054zCSV import ds1054z_wave as wave
import numpy as np
#from scipy import signal
import matplotlib.pyplot as plt



#Lowpass filter to remove color modulation.
#Takes voltage list in, outputs filtered voltage list
def lowpass(inputvoltage,alpha):
    datalength = len(inputvoltage)
    voltage_f = [0] * datalength
    voltage_f[0] = (alpha * inputvoltage[0])
    for i in range (1,datalength):
        voltage_f[i] = (voltage_f[i-1]+alpha*(inputvoltage[i] - voltage_f[i-1]))
    return voltage_f

#class ntsc_bwframe(object):
#   def __init__(self,inputwave):
#       self.image = np.array()

#Apply LPF with alpha = 0.001; ignore first ~8000 datapoints (LPF artifact);
#Look for first area under 0.30; Width is about 500 us (so about  2500 samples);
#Find minimum value in that period -- that is the rising edge of the vblank.
def find_vblankindex(inputvoltage):
    filteredvoltage = lowpass(inputvoltage,0.001)
    datalength = len(filteredvoltage)
    leftedge = 8000 #arbitrary left point to compensate for LPF weirdness
    while (filteredvoltage[leftedge] > 0.30):
        leftedge = leftedge + 1

    return np.argmin(filteredvoltage[leftedge:(leftedge+2500)]) + leftedge

def find_hsyncindices(inputvoltage,vblankindex):
    #Initially niave. Replace with better function!
    hsyncindices = []
    for i in range(6,400):
        hsyncindices.append(vblankindex+45+i*318)
    return hsyncindices
def readimage(inputvoltage,vblankindex,hsyncindeices,sizeX=300,sizeY=300):
    image = np.zeros((sizeY,sizeX))
    for y in range(1,sizeY-1):
        for x in range(1,sizeX-1):
            image[y][x] = inputvoltage[hsyncindices[y] + x]
    return image

wave1 = wave('data/ntsc.csv')
wave1.normalize()
vblankindex = find_vblankindex(wave1.voltage)
hsyncindices = find_hsyncindices(wave1.voltage,vblankindex)
print len(hsyncindices)
print hsyncindices[len(hsyncindices)-1]
decode = readimage(wave1.voltage,vblankindex,hsyncindices)
plt.imsave("decode.png",decode,cmap="binary")



#plt.plot(wave1.timestamp,wave1.voltage,'r-')
#plt.axvline(x=find_vblankindex(wave1.voltage)*wave1.timestep)
#plt.plot(wave1.timestamp,lowpass(wave1.voltage,0.1),'g-') #Use this waveform for greyscale
#plt.plot(wave1.timestamp,lowpass(wave1.voltage,0.005),'b-')
#plt.xlabel('Time ($\mu s$)')
#plt.ylabel('Signal Level (Normalized voltage)')
#plt.show()

print('NTSC Decoder -- J. Sheldon.')
print('Timestep: ' + str(wave1.timestep) + ' us')
print('Number of Points: ' + str(wave1.length))
print('Spanning a time of: '  + str(wave1.interval) + ' us')
