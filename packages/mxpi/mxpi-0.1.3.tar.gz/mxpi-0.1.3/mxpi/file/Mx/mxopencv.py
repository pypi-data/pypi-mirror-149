import cv2
import numpy as np

def color(value):
  digit = list(map(str, range(10))) + list("ABCDEF")
  value = value.upper()
  if isinstance(value, tuple):
    string = '#'
    for i in value:
      a1 = i // 16
      a2 = i % 16
      string += digit[a1] + digit[a2]
    return string
  elif isinstance(value, str):
    a1 = digit.index(value[1]) * 16 + digit.index(value[2])
    a2 = digit.index(value[3]) * 16 + digit.index(value[4])
    a3 = digit.index(value[5]) * 16 + digit.index(value[6])
    return (a3, a2, a1)

def color_block(frame,color):
    h_min=color[0]
    s_min=color[1]
    v_min=color[2]
    h_max=color[3]
    s_max=color[4]
    v_max=color[5]
    
    imgHsv=frame
    #imgHsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHsv,lower,upper)
    ret, binary = cv2.threshold(mask,0,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(binary,mode=cv2.RETR_TREE,method=cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        return [x,y,w,h]
    else:
    	return [0,0,0,0]
    	
def rectangle(frame,z,colors,size):
    frame=cv2.rectangle(frame,(int(z[0]),int(z[1])),(int(z[0]+z[2]),int(z[1]+z[3])),color(colors),size)
    return frame
    
def circle(frame,xy,rad,colors,tk):
    frame=cv2.circle(frame,xy,rad,color(colors),tk)
    return frame

def line(frame,stxy,endxy,colors,size):
    frame=cv2.line(frame, stxy, endxy,color(colors), size)
    return frame

def text(frame,text,xy,font_size,colors,size):
    frame=cv2.putText(frame,  text, xy, cv2.FONT_HERSHEY_SIMPLEX, font_size, color(colors),size)
    return frame

def find_camid():
    print('开始测试摄像头,请耐心等待...')
    a=[]
    for i in range(0,2000):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            a.append(i)
        else:
            pass
    print('ID列表：'+str(a))
