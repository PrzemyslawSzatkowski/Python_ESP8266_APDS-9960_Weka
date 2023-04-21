from time import sleep
from micropython import const

class I2CEX:
    def __init__(self,i2c,address):
        self.__i2c=i2c
        self.__address=address
    def __regWriteBit(self,reg,bitPos,bitVal):
        val=self.__readByte(reg)
        if bitVal == True:
            val=val | (1<<bitPos)
        else:
            val=val & ~(1<<bitPos)
        self.__writeByte(reg,val)
    def __writeByte(self,reg,val):
        self.__i2c.writeto_mem(self.__address,reg,bytes((val,)))
    def __readByte(self,reg):
        val =self.__i2c.readfrom_mem(self.__address,reg, 1)
        return int.from_bytes(val, 'big', True)
    def __write2Byte(self,reg,val):
        b = bytearray(2)
        b[0]=val & 0xff
        b[1]=(val>>8) & 0xff
        self.__i2c.writeto_mem(self.__address,reg,b)
    def __read2Byte(self,reg):
        val =self.__i2c.readfrom_mem(self.__address,reg,2)
        return int.from_bytes(val, 'little', True)

class ALS(I2CEX):
    def __init__(self,i2c):
        super().__init__(i2c,0x39)
    def enableSensor(self,on=True):
        AEN=1
        super().__regWriteBit(reg=0x80,bitPos=AEN,bitVal=on)
    @property
    def eLightGain(self):
        val=super().__readByte(0x8f)
        val= val & 0b00000011 
        return val
    @eLightGain.setter
    def eLightGain(self,eGain):
        val=super().__readByte(0x8f)
        eGain &= 0b00000011
        val &= 0b11111100
        val |= eGain
        super().__writeByte(0x8f,val)
    @property
    def ambientLightLevel(self):
        return super().__read2Byte(0x94)
    @property
    def redLightLevel(self):
        return super().__read2Byte(0x96)
    @property
    def greenLightLevel(self):  
        return super().__read2Byte(0x98)
    @property
    def blueLightLevel(self):    
        return super().__read2Byte(0x9A)

class PROX(I2CEX):   
    def __init__(self,i2c):
        super().__init__(i2c,0x39)
    def enableSensor(self,on=True):
        PEN=2
        super().__regWriteBit(reg=0x80,bitPos=PEN,bitVal=on)
    @property
    def eProximityGain(self):
        val=super().__readByte(0x8f)
        val=((val >>2) & 0b00000011) 
        return val
    @eProximityGain.setter
    def eProximityGain(self,eGain):
        val=super().__readByte(0x8f)
        eGain &= 0b00000011
        eGain = eGain << 2
        val &= 0b11110011
        val |= eGain
        super().__writeByte(0x8f,val)
    @property
    def eLEDCurrent(self):
        val=super().__readByte(0x8f)
        val=val >>6
        return val
    @eLEDCurrent.setter
    def eLEDCurrent(self,eCurent):
        val=super().__readByte(0x8f)        
        eCurent &= 0b00000011
        eCurent = eCurent << 6
        val &= 0b00111111
        val |= eCurent
        super().__writeByte(0x8f,val)
    @property
    def proximityLevel(self):  
        return super().__readByte(0x9c)

class APDS9960LITE(I2CEX):
    def __init__(self,i2c):      
        super().__init__(i2c,0x39)
        self.powerOn(False)
        sleep(.05)
        self.powerOn(True)
        self.prox=PROX(i2c)
        self.als=ALS(i2c)   
    prox = None
    als = None
    def powerOn(self,on=True):
        PON=0
        super().__regWriteBit(reg=0x80,bitPos=PON,bitVal=on)
    @property
    def statusRegister(self):
            return super().__readByte(0x93)