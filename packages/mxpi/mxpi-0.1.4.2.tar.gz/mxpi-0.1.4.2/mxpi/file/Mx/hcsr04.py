from hcsr04sensor import sensor
from threading import Thread

class mThread (Thread):
    def __init__(self, trig,echo):
        Thread.__init__(self)
        self.trig=trig
        self.echo=echo
        self.va=0
    def run(self):
        value = sensor.Measurement(self.trig, self.echo)
        while 1:
            raw_measurement = value.raw_distance(sample_size=5, sample_wait=0)
            self.va=round(raw_measurement, 1)
            
class init():
    def __init__(self,trig,echo):
        self.trig=trig #send-pin
        self.echo=echo #receive-pin
        self.run=mThread(self.trig,self.echo)
        self.run.start()
    def read(self):
        return self.run.va