import smbus
import time

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

class scripts:
    RGB = 1
    WHITE_FLASH = 2
    RED_FLASH = 3
    GREEN_FLASH = 4
    BLUE_FLASH = 5
    CYAN_FLASH = 6
    MAGENTA_FLASH = 7
    YELLOW_FLASH = 8
    

class blinkm:
    """
    A blinkm class for the Raspberry Pi.
    
    Attributes:
        address    The address of the blinkm device 
    """
    def __init__(self,address = 0x9):
        self.bus = smbus.SMBus(1)
        self.address = address

    def fadeToRGB(self,color: tuple):
        """
        Immediately sets the RGB colour to the LED
        """
        r,g,b = color
        self._sendi2c('c',[r,g,b])

    def goToRGB(self,color: tuple) -> None:
        """
        Immediately sets the RGB colour to the LED
        """
        r,g,b = color
        self._sendi2c('n',[r,g,b])

    def playScript(self,script,repeats=0,start=0):
        self.goToRGB((0,0,0))
        self.setFadeSpeed(16)
        self._sendi2c('t',[0])
        self._sendi2c('p',[script,repeats,start])
        self._sendi2c('t',[5])

    def setFadeSpeed(self,speed):
        """ 
        Set the fade speed of the blinkm
        """
        speed = clamp(speed,1,255)
        self._sendi2c('f',[speed])

    def _sendi2c(self,command,data=[]) -> None:
        """
        Sends a block of data with the command byte.
        """
        if isinstance(command,str):
            command = ord(command)
        try:
            self.bus.write_i2c_block_data(self.address,command,data)
        except OSError as err:
            print("I2C Device Error\nCheck Connection\n{}".format(err))

    def stopScript(self):
        self._sendi2c('o')

    def reset(self):
        self.goToRGB((0,0,0))

if __name__ == '__main__':

    ## Define some colors to use
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)

    ## Create a sequence of colors
    seq = [RED,GREEN,BLUE]

    ## Connect the blinkm (default address is 0x09)
    ADDR = 0x09
    bm = blinkm(ADDR)

    ## Go to each color in the sequence with a 2 second gap
    ##for color in seq:
    ##    bm.goToRGB(color)
    ##    time.sleep(2)#

    ## Set the Fade Speed to 1
    ##bm.setFadeSpeed(1)

    ## Fade to each color in the sequence
    ##for color in seq:
    ##    bm.fadeToRGB(color)
    ##    time.sleep(3)

    ##bm.reset()
    bm.playScript(scripts.BLUE_FLASH)
    time.sleep(5)
    bm.stopScript()
