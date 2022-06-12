import csv

class Spectrum:
    def __init__(self, motor: str, speed, ang):
        assert motor in MotorsParameters.fanData.keys(), "Motor not listed."
        assert int(speed) in MotorsParameters.fanData[motor], "This motor does not have that speed."
        assert int(ang) in MotorsParameters.angles, "Angle not listed."

        self.__motor = motor  # motor name
        self.__speed = int(speed)  # motor speed
        self.__angle = int(ang)  # motor angle
        self.__SPL = self._modelSPL()  # SPL
        self.__freq = self._modelFreq()  # Frequence

    def getMotor(self):
        return self.__motor

    def getSpeed(self):
        return self.__speed

    def getAngle(self):
        return self.__angle

    def getSPL(self):
        return self.__SPL

    def getFreq(self, nominal=False):
        if nominal:
            frequence = list()

            for i, item in enumerate(self.__freq):
                frequence.append(self._mapToNominal(item))

            return frequence

        return self.__freq

    @staticmethod
    def _mapToNominal(freq):
        '''This function find the closiest one-third octave frequency band'''

        freq = float(freq)

        for i, item in enumerate(MotorsParameters.nominalFrequences):
            if i == 0:
                tmp = (freq - item)**2

            else:
                distance = (freq - item)**2
                if distance > tmp:
                    return MotorsParameters.nominalFrequences[i-1]

                tmp = distance

        return MotorsParameters.nominalFrequences[-1]

    def _modelInfo(self, type: str, angle):
        '''This function accesses the archives by angle and return the SPLs or the frequences'''

        assert type in ['SPL', 'freq'], "type parameter is incorrect"

        info = list()
        local = ''
        for i in range(len(__file__)-1, -1, -1):
            if __file__[i] == '\\':
                for j in range(i):
                    local = local + __file__[j]
                break
            
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

    def _modelFreq(self):
        '''Get the frequence of all angles'''

        Freq = (self._modelInfo("freq", self.__angle))

        return Freq

    def getArray(self, nominal=False):
        heidmannDB = list()

        if nominal:
            for i, item in enumerate(self.__SPL):
                tmp = list()

                tmp.append(self.__motor)
                tmp.append(self.__speed)
                tmp.append(self.__angle)
                tmp.append(self._mapToNominal(self.__freq[i]))
                tmp.append(item)

                heidmannDB.append(tmp)

        else:
            for i, item in enumerate(self.__SPL):
                tmp = list()

                tmp.append(self.__motor)
                tmp.append(self.__speed)
                tmp.append(self.__angle)
                tmp.append(self.__freq[i])
                tmp.append(item)

                heidmannDB.append(tmp)

        return heidmannDB


class Motor():
    def __init__(self, motor):
        assert motor in MotorsParameters.fanData.keys(), "Motor not listed."
        self.__motor = motor

    def getMotor(self):
        return self.__motor
    
    def getSpeed(self):
        return MotorsParameters.fanData[self.__motor]
    
    def getArray(self, nominal=False):
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
        allSpectre = list()
        
        for motor in MotorsParameters.fanData.keys():
            motorArray = Motor(motor).getArray(nominal)
            for i in motorArray:                
                allSpectre.append(i)
            
        return allSpectre

class MotorsParameters:

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

    fanData = {"FanA": [60, 70, 80, 90],
               "FanB": [60, 70, 80, 90],
               "FanC": [60, 70, 80, 90],
               "FanQF_1": [60, 70, 80, 90],
               "FanQF_3": [60, 70, 80, 90],
               "FanQF_5": [60, 70, 80, 85],
               "FanQF_6": [60, 70, 80, 90],
               "FanQF_9": [60, 70, 86, 93]}

    fanDatabySpeed = {60: ["FanA", "FanB", "FanC", "FanQF_1", "FanQF_3", "FanQF_5",
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
    def allMotors():
        MotorsParameters.motorsParameters = dict()
        for motor in MotorsParameters.fanData.keys():
            MotorsParameters.motorsParameters[motor] = MotorsParameters.singleMotor(
                motor)

        return MotorsParameters.motorsParameters

    @staticmethod
    def singleMotor(motor: str):
        motorParam = dict()

        for param, values in MotorsParameters.paramsDict.items():
            motorParam[param] = values[list(
                MotorsParameters.fanData.keys()).index(motor)]

        return motorParam