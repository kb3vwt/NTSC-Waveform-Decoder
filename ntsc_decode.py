from DS1054zCSV import ds1054z_wave as wave
import numpy as np
#from scipy import signal
import matplotlib.pyplot as plt

#Lowpass filter to remove color modulation
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

#def find_vblank(inputwave):






wave1 = wave('data/ntsc.csv')
wave1.normalize()




plt.plot(wave1.timestamp,wave1.voltage,'r-')
wave1.voltage = lowpass(wave1.voltage,0.1)
plt.plot(wave1.timestamp,wave1.voltage,'b-')
plt.xlabel('Time ($\mu s$)')
plt.ylabel('Signal Level (Normalized voltage)')
plt.show()

print('NTSC Decoder -- J. Sheldon.')
print('Timestep: ' + str(wave1.timestep) + ' us')
print('Number of Points: ' + str(wave1.length))
print('Spanning a time of: '  + str(wave1.interval) + ' us')
