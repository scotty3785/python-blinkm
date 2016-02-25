import smbus
import time

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class blinkm:
    def __init__(self,address):
        self.bus = smbus.SMBus(1)
        self.address = address

    def fadeToRGB(self,color):
        """fadeToRGB((r,g,b))
        Immediately sets the RGB colour to the LED"""
        r,g,b = color
        self._sendi2c('c',[r,g,b])

    def goToRGB(self,color):
        """goToRGB((r,g,b))
        Immediately sets the RGB colour to the LED"""
        r,g,b = color
        self._sendi2c('n',[r,g,b])

    def setFadeSpeed(self,speed):
        """ setFadeSpeed(seconds)
        BlinkM used 1/30 seconds as a tick time
        we use seconds. 255 = 1/30 seconds, 1 = 8.5 seconds
        This function converts seconds to ticks"""
        speed = 255 - int(speed / (1/30))
        speed = clamp(speed,1,255)
        print("Speed: {}".format(speed))
        self._sendi2c('f',[speed])

    def _sendi2c(self,command,data):
        """_sendi2c(command,data)
        Sends a block of data with the command byte."""
        if isinstance(command,str):
            command = ord(command)
        self.bus.write_i2c_block_data(self.address,command,data)


if __name__ == '__main__':

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    seq = [RED,GREEN,BLUE]

    ADDR = 0x09
    bm = blinkm(ADDR)

    for color in seq:
        bm.goToRGB(color)
        time.sleep(2)#

    bm.setFadeSpeed(1)

    for color in seq:
        bm.fadeToRGB(color)
        time.sleep(3)
    


##    bm.goToRGB((255,0,0))
##    time.sleep(2)
##    bm.goToRGB((0,255,0))
##    time.sleep(2)
##    bm.goToRGB((0,0,255))

    #bus = smbus.SMBus(1)

    ##To play a script
    ##Command Byte, Script Number, Repeats, Start Playing @ Start,


    #data1 = [0x70, 0x02, 0x03, 0x00]
    #data = [0x00, 0xFF, 0x00]
    #command = ord('n')
    #bus.write_i2c_block_data(ADDR,command,data)
