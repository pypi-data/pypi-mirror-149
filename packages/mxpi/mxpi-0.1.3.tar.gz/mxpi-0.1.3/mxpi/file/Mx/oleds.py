# -*- coding: utf-8 -*-
import Mx,os
from Mx.core.interface.serial import i2c, spi
from Mx.core.render import canvas,canvas_s
from Mx.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from Mx.core.virtual import viewport
from PIL import ImageFont,Image
from time import sleep

class i2c_init():
    def __init__(self,types,addr,port,background_color='black',w=128,h=64):
        self.serial = i2c(port=port, address=addr)
        self.w=w
        self.h=h
        if types=='ssd1306':
            self.device = ssd1306(self.serial, width=w, height=h)
        elif types=='ssd1331':
            self.device = ssd1331(self.serial, width=w, height=h)
        elif types=='ssd1325':
            self.device = ssd1325(self.serial, width=w, height=h)
        elif types=='sh1106':
            self.device = sh1106(self.serial, width=w, height=h)
        self.s=canvas(self.device,background_color=background_color)
        self.virtual = viewport(self.device, width=500, height=768)
        self.ss=canvas(self.virtual)
        
    def texts(self,xy,txt,color,font,f_size):
        font = ImageFont.truetype(os.path.dirname(Mx.__file__)+'/'+font, f_size)
        self.s.enter().text(xy, txt, fill=color,font=font)
        #example   s.texts((20,0),'显示汉字','#000','msyh.ttc',13)
        
    def ellipse(self,xy_xy,line_color,fill_color):
        self.s.enter().ellipse(xy_xy, outline=line_color, fill=fill_color)
    
    def rect(self,xy_xy,line_color,fill_color):
        self.s.enter().rectangle(xy_xy, outline=line_color, fill=fill_color)
    
    def polygon(self,xy_xy_xy,line_color,fill_color):
        self.s.enter().polygon(xy_xy_xy, outline=line_color, fill=fill_color)
    
    def line(self,xy_xy,color):
        self.s.enter().line(xy_xy, fill=color)
    
    def horizontal_scroll(self,txt,time,font,f_size):
        self.virtual = viewport(self.device, width=500, height=768)
        self.ss=canvas(self.virtual)
        font = ImageFont.truetype(os.path.dirname(Mx.__file__)+'/'+font, f_size)
        for i, line in enumerate(txt.split("n")):
            self.ss.enter().text((0, (i * 16)), text=line, fill="white", font=font)
        self.ss.show()
        # update the viewport one position below, causing a refresh,
        # giving a rolling up scroll effect when done repeatedly
        y = 0
        for x in range(240):
            self.virtual.set_position((x, y))
            sleep((1000/time)/1000)
    
    def vertical_scroll(self,txt,time,font,f_size):
        self.virtual = viewport(self.device, width=500, height=768)
        self.ss=canvas(self.virtual)
        font = ImageFont.truetype(os.path.dirname(Mx.__file__)+'/'+font, f_size)
        for i, line in enumerate(txt.split("n")):
            self.ss.enter().text((0, 20 + (i * 16)), text=line, fill="white", font=font)
        # update the viewport one position below, causing a refresh,
        # giving a rolling up scroll effect when done repeatedly
        self.ss.show()
        x = 0
        for y in range(240):
            self.virtual.set_position((x, y))
            sleep((10000/time)/1000)
            
    def display_img(self,url,w,h):
        logo = Image.open(url).convert("RGBA")
        logo = logo.resize((w,h),Image.ANTIALIAS)
        fff = Image.new(logo.mode, logo.size, (255,) * 4)
        background = Image.new("RGBA", self.device.size, "white")
        posn = ((self.device.width - logo.width) // 3, 0)
        rot = logo
        img = Image.composite(rot, fff, rot)
        background.paste(img, posn)
        self.device.display(background.convert(self.device.mode))
    
    def show(self):
        self.s.show()
        
    def clear(self):
        self.s.clear()

if __name__=="__main__":
    s=i2c_init('ssd1306',0x3C,1,'black')


