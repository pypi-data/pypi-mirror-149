import RPi.GPIO as GPIO
import time
from threading import Thread

class mThread (Thread):
    def __init__(self, trig,echo):
        Thread.__init__(self)
        self.trig=trig
        self.echo=echo
        self.value=0
    def run(self):
         while 1:
            GPIO.output(self.trig,True)
            time.sleep(0.00001) #1us
            GPIO.output(self.trig,False)
            while GPIO.input(self.echo)==0:
                pass
            start=time.time()
            while GPIO.input(self.echo)==1:
                pass
            end=time.time()
            distance=round((end-start)*343/2*100,2)
            time.sleep(0.1)
            self.value=distance
            
class init():
    def __init__(self,trig,echo):
        self.trig=trig #send-pin
        self.echo=echo #receive-pin
        GPIO.setup(self.trig,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(self.echo,GPIO.IN)
        self.run=mThread(self.trig,self.echo)
        self.run.start()
    def read(self):
        return self.run.value