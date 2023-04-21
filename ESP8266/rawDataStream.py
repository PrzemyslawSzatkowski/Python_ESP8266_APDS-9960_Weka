import machine
from time import sleep_ms,time_ns
from apds9960 import APDS9960LITE

machine.freq(160000000)
I2C=machine.I2C(scl=machine.Pin(5),sda=machine.Pin(4))
apds9960=APDS9960LITE(I2C)

apds9960.als.enableSensor(True) #Light sensor on
apds9960.als.eLightGain=3 #light sensor gain [1x, 2x, 16x, 64x]

apds9960.prox.enableSensor(True) #Proximity sensor on
apds9960.prox.eProximityGain=3 #Proximity sensor gain [1x, 2x, 4x, 8x]

apds9960.prox.eLEDCurrent=0 #LED current [100 mA, 50 mA, 25 mA, 12.5 mA]

LED=machine.Pin(2, machine.Pin.OUT) #Onboard LED set

clear=True #zmienna do badania ciągłości
sleep_ms(10) #Wait for initiate
while True:
        sleep_ms(7)
        if apds9960.prox.proximityLevel > 5: #Prox lvl statement
            LED.off() #Włączenie LED
            print(
                #time_ns(), #Wyświetlenie czasu sys
                apds9960.als.redLightLevel, #Czerwony
                apds9960.als.greenLightLevel, #Zielony
                apds9960.als.blueLightLevel, #Niebieski
                apds9960.als.ambientLightLevel, #Biały
                apds9960.prox.proximityLevel) #Prox lvl
            if clear == True:
                clear = False
        else:
            LED.on()
            if clear == False:
                clear = True
                print()