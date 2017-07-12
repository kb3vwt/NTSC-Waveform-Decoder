#ds1054z_wave:
#Takes csv file from Rigol DS1054z, puts voltages and timestamps into lists:
#ds1054z_wave.voltage[] and ds1054z_wave.timestamp[].
#Number of points accessible through ds1054z_wave.length
#Total interval is accessible through ds1054z_wave.interval
class ds1054z_wave(object):
    def __init__(self,filename):
        self.voltage = []
        self.timestamp = []
        self.timestep = 0.0
        self.length = 0
        self.interval = 0.0

        #Read in unprepared CSV file from Rigol DS1054z:
        with open(filename,'r') as csv:
            csvline = csv.readlines()
        csv.close()

        #Get timestep from header:
        self.timestep = float(csvline[1].split(',')[3].rstrip()) * 1000000

        #split lines, fill voltages:
        csvline_split= []
        for i in range(2,len(csvline)):
            csvline_split = csvline[i].split(",")
            self.voltage.append(float(csvline_split[1].rstrip()))
        self.length = len(self.voltage)

        #populate timestamps
        for i in range(0,self.length):
            self.timestamp.append(self.timestep*i)

        #Calculate interval
        self.interval = self.timestamp[self.length-1]
        #Create empty array of filtered voltages:
        self.voltage_f = [0] * self.length
    def normalize(self,A=1):
        maxvoltage = max(self.voltage)
        for i in range(0,self.length):
            self.voltage[i] = A * self.voltage[i] / maxvoltage



def lowpass(self,inputwave,alpha):
    datalength = len(inputwave.voltage)
    voltage_f[0] = (alpha * inputwave.voltage[0])
    for i in range (1,datalength):
        voltage_f[i] = (voltage_f[i-1]+alpha*(inputwave.voltage[i] - voltage_f[i-1]))
    return voltage_f
