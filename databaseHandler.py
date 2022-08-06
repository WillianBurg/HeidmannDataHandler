'''Helps to manipulate spectrum data from Heidmann model,
see references at https://aerospacemodel.paginas.ufsc.br/heidmann-data-set-willian/

Author: Willian Alexsander Burg
'''

import csv
import math

class MotorsParameters:
    '''A miscellaneous class, gathering multiples variables for the library to work.
    
    Atributes:
        None
    '''
    
    #In order: FanA, FanB, FanC, FanQF_1, FanQF_3, FanQF_5, FanQF_6, FanQF_9
    paramsDict = {
        "TotalPressure": [1.5, 1.5, 1.6, 1.5, 1.4, 1.6, 1.2, 1.2],
        "MassFlow":      [430, 430, 415, 396, 396, 385, 396, 403],
        "MT":            [1.04, 1.04, 1.39, 0.99, 0.99, 0.89, 0.67, 0.63],
        "MTd":           [1.2, 1.2, 1.52, 1.12, 1.12, 1.14, 0.88, 0.87],
        "V":             [90, 60, 60, 112, 112, 88, 50, 11],
        "B":             [40, 26, 26, 53,  53, 36, 42, 15],
        "BPF":           [2420, 1570, 2250, 3120, 3120, 2180, 1670, 556],
        "Cutoff":        [0.83, 0.8, 0, 0.89, 0.89, 0.68, 3.53, 2.38],
        "RSS":           [200, 200, 200, 367, 367, 227, 400, 200]
    }
    
    Fanid = ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_5",
                           "FanQF_6", "FanQF_9"]
    
    speedsByFan = {"FanA": [60, 70, 80, 90],
               "FanB": [60, 70, 80, 90],
               "FanC": [60, 70, 80, 90],
               "FanQF_1": [60, 70, 80, 90],
               "FanQF_3": [60, 70, 80, 90],
               "FanQF_5": [60, 70, 80, 85],
               "FanQF_6": [60, 70, 80, 90],
               "FanQF_9": [60, 70, 86, 93]}

    fanBySpeeds = {60: ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_5",
                           "FanQF_6", "FanQF_9"],
                      70: ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_5",
                           "FanQF_6", "FanQF_9"],
                      80: ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_5",
                           "FanQF_6"],
                      85: ["FanQF_5"],
                      86: ["FanQF_9"],
                      90: ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_6"],
                      93: ["FanQF_9"]}

    angles = [10, 20, 30, 40, 50, 60, 70, 80,
              90, 100, 110, 120, 130, 140, 150, 160]

    nominalFrequences = [50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000,
                         1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500,
                         16000, 20000]

    def __init__(self):
        pass

    @staticmethod
    def singleMotor(motor: str):
        '''Returns a dictionary with the parameters from the given motor'''
        
        motorParam = dict()

        # Build a dict for the motor with paramsDict
        for param, values in MotorsParameters.paramsDict.items():
            motorParam[param] = values[list(MotorsParameters.Fanid).index(motor)]

        return motorParam

    @staticmethod
    def allMotors():
        '''Returns a dictionary with the parameters from all motors'''
        
        motorsParams = dict()
        
        for motor in MotorsParameters.Fanid: # Appends every motor dict on a new dict
            motorsParams[motor] = MotorsParameters.singleMotor(motor)

        return motorsParams

class Spectrum:
    '''A class that represents a spectrum
    
    Atributes:
        motor: str
            Motor spectrum, see MotorsParameters.speedsByFan list
        speed : str/int 
            Speed spectrum, see MotorParameters.speedsByFan list
        ang : str/int
            Angle spectrum, see MotorParameters.speedsByFan list
    '''
    
    def __init__(self, motor: str, speed, ang):
        '''Checks the parameters and stores the variables, as well SPL and frequencies'''
        
        assert motor in MotorsParameters.Fanid, "Motor not listed."
        assert int(speed) in MotorsParameters.speedsByFan[motor], "This motor does not have that speed."
        assert int(ang) in MotorsParameters.angles, "Angle not listed."

        self.__motor = motor  # motor name
        self.__speed = int(speed)  # motor speed
        self.__angle = int(ang)  # motor angle
        self.__SPL = self._modelSPL()  # SPL
        self.__freq = self._modelFreq()  # Frequence
        self.__normal = self._modelNormal() # Normalized SPL

    def getMotor(self):
        '''Returns the motor's name'''
        
        return self.__motor

    def getSpeed(self):
        '''Returns the spectrum's speed'''
        
        return self.__speed

    def getAngle(self):
        '''Returns the spectrum's angle'''
        
        return self.__angle

    def getSPL(self):
        '''Returns a list with spectrum's SPL on frequence order'''
        
        return self.__SPL
    
    def getNormal(self):
        '''Returns a list with spectrum's SPL normalized on frequence order'''

        return self.__normal

    def getFreq(self, nominal=False):
        '''Returns a list with spectrum's frequence on one-third octave frequency band order'''
        
        if nominal: # Checks the parameter
            frequence = list()

            for item in enumerate(self.__freq):
                frequence.append(self._mapToNominal(item)) # Search for nominal frequence correspondent

            return frequence

        return self.__freq

    @staticmethod
    def _mapToNominal(freq):
        '''This function find the closest one-third octave frequency band'''

        freq = float(freq)

        for i, item in enumerate(MotorsParameters.nominalFrequences):
            if i == 0:
                tmp = (freq - item) ** 2

            else:
                distance = (freq - item) ** 2
                if distance > tmp:
                    return MotorsParameters.nominalFrequences[i-1]

                tmp = distance

        return MotorsParameters.nominalFrequences[-1]

    def _modelInfo(self, type: str, angle):
        '''This function accesses the archives by angle and return the SPLs or the frequences'''

        assert type in ['SPL', 'freq'], "type parameter is incorrect"

        # Get the local file, erase until first '\' and add 'models' to find the models files.
        info = list()
        local = ''
        for i in range(len(__file__)-1, -1, -1):
            if __file__[i] == '\\':
                for j in range(i):
                    local = local + __file__[j]
                break
        
        # Local where the files are  
        csvLocal = f'{local}\models\{self.__motor}-{self.__speed}Sp-Ang{angle}.dat'
        with open(csvLocal, 'r') as file:
            data = csv.DictReader(file)

            for item in data:
                info.append(float(item[type]))

        return info

    def _modelSPL(self):
        '''Get the SPL of all angles'''

        SPL = (self._modelInfo("SPL", self.__angle))

        return SPL
    
    def _modelNormal(self):
        '''Normalizes the SPL for all frequences'''
        
        SPL_normal = list()
        
        for item in self.__SPL:
            SPL_normal.append(Normal(self.__motor, self.__speed, self.__angle, item).SPL_normal)
        
        return SPL_normal
        
    def _modelFreq(self):
        '''Get the frequence of all angles'''

        Freq = (self._modelInfo("freq", self.__angle))

        return Freq

    def getArray(self, nominal=False):
        '''Returns an array with motor's name, speed, angle, frequence and SPL on each list'''
        
        heidmannDB = list()

        if nominal:
            for i, item in enumerate(self.__SPL):
                tmp = list()

                tmp.append(self.__motor)
                tmp.append(self.__speed)
                tmp.append(self.__angle)
                tmp.append(self._mapToNominal(self.__freq[i]))
                tmp.append(item)
                tmp.append(Normal(self.__motor, self.__speed, self.__angle, item).SPL_normal)

                heidmannDB.append(tmp)

        else:
            for i, item in enumerate(self.__SPL):
                tmp = list()

                tmp.append(self.__motor)
                tmp.append(self.__speed)
                tmp.append(self.__angle)
                tmp.append(self.__freq[i])
                tmp.append(item)
                tmp.append(Normal(self.__motor, self.__speed, self.__angle, item).SPL_normal)

                heidmannDB.append(tmp)

        return heidmannDB


class Motor():
    '''A class that represents all spectrums from a motor
    
    Atributes:
        motor: str
            Motor spectrum, see MotorsParameters.speedsByFan list
    '''
        
    def __init__(self, motor):
        '''Checks the parameters and store the variables'''
        
        assert motor in MotorsParameters.Fanid, "Motor not listed."
        
        self.__motor = motor

    def getMotor(self):
        '''Returns the motor's name'''
        
        return self.__motor
    
    def getSpeed(self):
        '''Returns the speed's name'''
        
        return MotorsParameters.speedsByFan[self.__motor]
    
    def getArray(self, nominal=False):
        '''Returns all arrays from all spectrums that motor has'''
        
        speeds = self.getSpeed()
        motorSpectre = list()
        
        for speedIter in range(len(speeds)):
            for angIter in range(len(MotorsParameters.angles)):
                specArray = Spectrum(self.__motor, speeds[speedIter], MotorsParameters.angles[angIter]).getArray(nominal)
                
                for i in range(len(specArray)):                    
                    motorSpectre.append(specArray[i])
                    
        return motorSpectre
    
    @staticmethod
    def getAll(nominal=False):
        '''Return all arrays from all spectrums'''
        
        allSpectre = list()
        
        for motor in MotorsParameters.Faind:
            motorArray = Motor(motor).getArray(nominal)
            for i in motorArray:                
                allSpectre.append(i)
            
        return allSpectre

class Normal:
    '''A class that normalizes the SPL
    
        motor: str
            Motor spectrum, see MotorsParameters.speedsByFan list
        speed : str/int 
            Speed spectrum, see MotorParameters.speedsByFan list
        ang : str/int
            Angle spectrum, see MotorParameters.speedsByFan list
        SPL : str/int
            SPL that will be normalized
    '''
    
    y = 1.4
    cte = (y-1) / y
    cte_inv = cte ** -1
    
    Tamb = (59 + 459.67) * 5/9

    def __init__(self, motor, speed, ang, SPL):
        self.motor = motor
        self.motorI = self.motorIndex()
        self.speed = int(speed)/100 #Convert int to percentage
        self.ang = int(ang)
        self.SPL = int(SPL)
        #From now on it is necessary to keep the function call order
        self.N = self.calcN()
        self.K = self.calcK()
        self.PR = self.calcPR()
        self.TR = self.calcTR()
        self.DT = self.calcDT()
        self.SPL_normal = self.calcSPL_normal()
    
    def motorIndex(self):
        '''Find the motor's index'''
        
        return MotorsParameters.Fanid.index(self.motor)
 
    def calcN(self):
        '''N is the axle rotation frequency '''
        
        motorBPF = MotorsParameters.paramsDict["BPF"][self.motorI]
        motorB = MotorsParameters.paramsDict["B"][self.motorI]        
        
        N = (motorBPF/motorB) * self.speed
    
        return N
        
    def calcK(self):        
        '''K in relation to pressure'''
        
        motorPressure = MotorsParameters.paramsDict["TotalPressure"][self.motorI]       
        
        k = (motorPressure ** (self.cte) -1) / self.N

        return k
    
    def calcPR(self):
        '''Pressure ratio'''
    
        PR = (1 + (self.K * self.N)) ** self.cte_inv
    
        return PR
    
    def calcTR(self):
        '''Temperature ratio'''
        
        TR = self.PR ** self.cte

        return TR
    
    def calcDT(self):
        '''Delta temperature'''
        
        DT = (self.TR - 1) * self.Tamb
        
        return DT
    
    def calcSPL_normal(self):
        '''Normalizes the SPL'''
        
        MF = MotorsParameters.paramsDict["MassFlow"][self.motorI]
        MFn = MF * self.speed
        SPL_normal = self.SPL - 20 * math.log10(self.DT/0.555) - 10 * math.log10(MFn/0.453)
        
        return SPL_normal