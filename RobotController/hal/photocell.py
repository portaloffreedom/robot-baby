from smbus import SMBus
from time import sleep

# Exception class for an I2C address out of bounds
class I2CaddressOutOfBoundsError(Exception):
    message = 'I2C Exception: I2C Address Out of Bounds'

# Exception class for a channel number out of bounds
class PCF8591PchannelOutOfBoundsError(Exception):
    message = 'PCF8591P Exception: ADC Channel Out of Bounds'

# Exception class for a DAC value out of bounds
class PCF8591PDACvalueOutOfBoundsError(Exception):
    message = 'PCF8591P Exception: DAC Output Value Out of Bounds'

class PCF8591P:

    # Constructor
    def __init__(self, __i2cBus, __addr):
        self.__bus = __i2cBus
        self.__addr = self.__checkI2Caddress(__addr)
        self.__DACEnabled = 0x00
    
    # Read single ADC Channel
    def readADC(self, __chan = 0):
        __checkedChan = self.__checkChannelNo(__chan)
        self.__bus.write_byte(self.__addr, __checkedChan  | self.__DACEnabled)
        __reading = self.__bus.read_byte(self.__addr) # need to throw away first reading
        __reading = self.__bus.read_byte(self.__addr) # read A/D
        return __reading
    
    # Read all ADC channels
    def readAllADC(self):
        __readings = []
        self.__bus.write_byte(self.__addr, 0x04  | self.__DACEnabled)
        __reading = self.__bus.read_byte(self.__addr) # need to throw away first reading
        for i in range (4):
            __readings.append(self.__bus.read_byte(self.__addr)) # read ADC
        return __readings   
    
    # Set DAC value and enable output
    def writeDAC(self, __val=0):
        __checkedVal = self.__checkDACVal(__val)
        self.__DACEnabled = 0x40
        self.__bus.write_byte_data(self.__addr, self.__DACEnabled, __checkedVal)
    
    # Enable DAC output    
    def enableDAC(self):
        self.__DACEnabled = 0x40
        self.__bus.write_byte(self.__addr, self.__DACEnabled)
    
    # Disable DAC output
    def disableDAC(self):
        self.__DACEnabled = 0x00
        self.__bus.write_byte(self.__addr, self.__DACEnabled)
    
    # Check I2C address is within bounds
    def __checkI2Caddress(self, __addr):
        if type(__addr) is not int:
            raise I2CaddressOutOfBoundsError
        elif (__addr < 0):
            raise I2CaddressOutOfBoundsError
        elif (__addr > 127):
            raise I2CaddressOutOfBoundsError
        return __addr

    # Check if ADC channel number is within bounds
    def __checkChannelNo(self, __chan):
        if type(__chan) is not int:
            raise PCF8591PchannelOutOfBoundsError
        elif (__chan < 0):
            raise PCF8591PchannelOutOfBoundsError
        elif (__chan > 3):
            raise PCF8591PchannelOutOfBoundsError
        return __chan

    # Check if DAC output value is within bounds
    def __checkDACVal(self, __val):
        if type(__val) is not int:
            raise PCF8591PDACvalueOutOfBoundsError
        elif (__val < 0):
            raise PCF8591PDACvalueOutOfBoundsError
        elif (__val > 255):
            raise PCF8591PDACvalueOutOfBoundsError
        return __val

# Test harnesses
if __name__ == "__main__":

    i2c = SMBus(1)

    try:
        sensor = PCF8591P(i2c, 0x48)
    except Exception as e:
        print ("Fail!!  Something went wrong!!" + e.message)

    sensor.enableDAC()
    sleep(1)
    
    while (1):
#          reading = sensor.readAllADC()
#          print (reading)
          reading = sensor.readADC(0)
          print ("0: {0}".format(reading))
          sleep(1)

