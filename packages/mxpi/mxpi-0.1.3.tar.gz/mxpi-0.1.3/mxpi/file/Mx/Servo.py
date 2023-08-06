import RPi.GPIO as gpio
import time

class gs90():
    def __init__(self,gpio_pin) -> None:
        self.gpio_pin = gpio_pin
        gpio.setup(gpio_pin, gpio.OUT) 
        self.gs90_pwm = gpio.PWM(gpio_pin, 50)  
        self.gs90_pwm.start(0)
        
    def turn(self,angle,t):
        if isinstance(angle, str):  # 判断数据类型
            if angle.upper() == 'STOP':
                self.gs90_pwm.ChangeDutyCycle(0)  
            else:
                print('输入有误')
        elif isinstance(angle, int) or isinstance(angle, float):  
            self.gs90_pwm.ChangeDutyCycle(2.5 + angle * 10 / 180)
            time.sleep(t)
            
if __name__ == '__main__':
	gpio.setmode(gpio.BCM)
	s=gs90(6)
	s.turn(90,0.5)

