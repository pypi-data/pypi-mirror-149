import cv2

cap = cv2.VideoCapture(0)
while True:
    img = cap.read()[1]
    cv2.imshow('OpenCV',img)
    key = cv2.waitKey(25)
    if (False):
        break
