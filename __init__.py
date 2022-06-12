from databaseHandler import *

if __name__ == "__main__":
    load = Spectrum("FanQF_9", "93", 10)
    a = MotorsParameters.allMotors()
    b = load.getSPL()
    c = load.getFreq(True)
    print(load.getArray(True))
    print(b)
    print(c)
    print(Motor("FanA").getArray(True))
    allarray = Motor("FanQF_3").getAll(True)

#Gists publicos não podem se tornar secretos porque o URL continua o mesmo, então não fica realmente secreto
#FanQF_5 60% 10° 50Hz->63Hz / 58Hz
#FanQF_5 60% 60° 200Hz->250Hz / 225.08Hz
#FALTOU O DE 160°
#FanQF_5 60% 160° Dado adicional: 1180Hz, Há um em 1250(1285) e outro em 1000(1010)
#FanQF_5 70% 40° Dado faltante: 1250Hz
#FanQF_5 70% 40° Dado adicional: 4150Hz, Há um mais próximo de 4000 e outro bem próximo de 5000
#FanQF_5 85% 80° 20000Hz->16000Hz / 17674Hz
#FanQF_6 80% 100° 2000Hz->1600Hz / 1782Hz
#FanQF_6 80% 120° 8000Hz->10000Hz / 9028Hz
"""def __init__(self, motor, speed):
    #Trabalha com a frequência nominal para padronizar
    if type(motor) == list:
        assert len(motor) >= 1, 'The list is empty'
        for i in motor:
            assert i in MotorsParameters.fanData.keys(), f"{i} is not listed."
            assert int(speed) in MotorsParameters.fanData[i], f"{i} does not have that speed."
        
        self.__motor = motor
        self.__speed = int(speed)
        
    else:
        assert motor in MotorsParameters.fanData.keys(), "Motor not listed."
        assert int(speed) in MotorsParameters.fanData[motor], "This motor does not have that speed."
        
        self.__motor = motor
        self.__speed = int(speed)
        
    def getMatrix(self, ang):
        matrix = [[0]*len(self.__motor) for _ in range (len(MotorsParameters.nominalFrequences))]

        for i, motor in enumerate(self.__motor):
            tmp = Spectrum(motor, self.__speed, ang).getSPL()
            
            for j, freq in enumerate(MotorsParameters.nominalFrequences):
                matrix[j][i] = tmp[j]
        
        return matrix, MotorsParameters.nominalFrequences, self.__motor"""