import smbus

class init():
    def __init__(self) -> None:
        self.address = 0x48
        self.bus = smbus.SMBus(1)
    def read(self,pin):
        if pin=='A0':
            addr=0x40 
        elif pin=='A1':
            addr=0x41
        elif pin=='A2':
            addr=0x42
        elif pin=='A3':
            addr=0x43
        self.bus.write_byte(self.address,addr)
        value=self.bus.read_byte(self.address)
        return value
    
    def write(self,value):
        self.bus.write_byte_data(self.address,0x40,value)