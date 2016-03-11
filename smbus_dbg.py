class SMBus:
    def __init__(self,bus):
        self.bus = bus

    def write_i2c_block_data(self,address,command,data):
        print("Writing to Device {}\nCommand: {}\nData: {}".format(hex(address),command,data))
