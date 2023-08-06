import RPi.GPIO as GPIO
import time
from threading import Thread
import Adafruit_DHT
class mThread (Thread):
    def __init__(self,dht,pin):
        Thread.__init__(self)
        self.pin=pin
        self.dht=dht
        self.value=(0,0)
    def run(self):
         while 1:
            self.value=Adafruit_DHT.read_retry(self.dht,self.pin)
            
class inits():
    def __init__(self,dht,pin):
        self.run=mThread(dht,pin)
        self.run.start()
    def read(self):
        #time.sleep(0.01)
        return self.run.value
    
if __name__=='__main__':
    s=inits(Adafruit_DHT.DHT11,17)
    while True:
        print(s.read())
    GPIO.cleanup();