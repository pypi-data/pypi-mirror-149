import RPi.GPIO as GPIO

from Mx.core.interface.serial import spi, noop
from Mx.core.render import canvas
from Mx.core.virtual import viewport
from Mx.led.device import max7219
from Mx.core.legacy import text, show_message
from Mx.core.legacy.font import proportional,CP437_FONT,ATARI_FONT,LCD_FONT,SEG7_FONT,SINCLAIR_FONT,SPECCY_FONT,TINY_FONT,UKR_FONT


class led_init():
    def __init__(self,width=8,height=8,w_num=1,h_num=1,block_orientation=0):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=width*w_num, height=height*h_num, block_orientation=block_orientation)
        self.virtual = viewport(self.device, width=width*w_num, height=height*h_num)
        self.s=canvas(self.virtual)
        
    def line(self,l):
        self.s.enter().line(l, fill="white")
            
    def point(self,l):
        self.s.enter().point(l, fill="white")
    
    def texts(self,texts,xy,font=ATARI_FONT):
        text(self.s.enter(), xy, texts, fill="white", font=proportional(font))
    
    def show(self):
        self.s.show()
    
    def show_text(self,text,font,sp):
        show_message(self.device, text, fill="white", font=proportional(font), scroll_delay=sp)
   
    def contrast(self,num):
        self.device.contrast(num)
    



