import cv2
import numpy as np
import argparse

class init():
    def __init__(self,model,classes,anchor,objThreshold=0.3, confThreshold=0.3, nmsThreshold=0.4):
        self.classes=classes
        self.stride = [16, 32]
        self.anchor_num = 3
        self.anchor=anchor
        self.model=model
        self.anchors = np.array(self.anchor,
                           dtype=np.float32).reshape(len(self.stride), self.anchor_num, 2)
        self.inpWidth = 352
        self.inpHeight = 352
        self.net = cv2.dnn.readNet(self.model)
        self.confThreshold = confThreshold
        self.nmsThreshold = nmsThreshold
        self.objThreshold = objThreshold
        
    def _make_grid(self, nx=20, ny=20):
        xv, yv = np.meshgrid(np.arange(ny), np.arange(nx))
        return np.stack((xv, yv), 2).reshape((-1, 2)).astype(np.float32)

    def run(self, frame):
        outs=self.detect(frame)
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        ratioh, ratiow = frameHeight / self.inpHeight, frameWidth / self.inpWidth
        # Scan through all the bounding boxes output from the network and keep only the
        # ones with high confidence scores. Assign the box's class label as the class with the highest score.
        classIds = []
        confidences = []
        boxes = []
        for detection in outs:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > self.confThreshold and detection[4] > self.objThreshold:
                center_x = int(detection[0] * ratiow)
                center_y = int(detection[1] * ratioh)
                width = int(detection[2] * ratiow)
                height = int(detection[3] * ratioh)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                # confidences.append(float(confidence))
                confidences.append(float(confidence*detection[4]))
                boxes.append([left, top, width, height])

        # Perform non maximum suppression to eliminate redundant overlapping boxes with
        # lower confidences.
        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confThreshold, self.nmsThreshold)
        msg=[]
        for i in indices:
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            msg.append({'id':classIds[i], 'Confidence':confidences[i], 'position':[left, top, left + width, top + height]})
            #frame = self.drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height)
        return msg

 
    def detect(self, srcimg):
        blob = cv2.dnn.blobFromImage(srcimg, 1 / 255.0, (self.inpWidth, self.inpHeight))
        self.net.setInput(blob)
        outs = self.net.forward(self.net.getUnconnectedOutLayersNames())[0]
        outputs = np.zeros((outs.shape[0]*self.anchor_num, 5+len(self.classes)))
        row_ind = 0
        for i in range(len(self.stride)):
            h, w = int(self.inpHeight / self.stride[i]), int(self.inpWidth / self.stride[i])
            length = int(h * w)
            grid = self._make_grid(w, h)
            for j in range(self.anchor_num):
                top = row_ind+j*length
                left = 4*j
                outputs[top:top + length, 0:2] = (outs[row_ind:row_ind + length, left:left+2] * 2. - 0.5 + grid) * int(self.stride[i])
                outputs[top:top + length, 2:4] = (outs[row_ind:row_ind + length, left+2:left+4] * 2) ** 2 * np.repeat(self.anchors[i, j, :].reshape(1,-1), h * w, axis=0)
                outputs[top:top + length, 4] = outs[row_ind:row_ind + length, 4*self.anchor_num+j]
                outputs[top:top + length, 5:] = outs[row_ind:row_ind + length, 5*self.anchor_num:]
            row_ind += length
        return outputs


if __name__ == '__main__':
    anchor=[12.64, 19.39, 37.88, 51.48, 55.71, 138.31, 126.91, 78.23, 131.57, 214.55, 279.92, 258.87]
    model = init('model.onnx',['person',
'bicycle',
'car',
'motorbike',
'aeroplane',
'bus',
'train',
'truck',
'boat',
'traffic light',
'fire hydrant',
'stop sign',
'parking meter',
'bench',
'bird',
'cat',
'dog',
'horse',
'sheep',
'cow',
'elephant',
'bear',
'zebra',
'giraffe',
'backpack',
'umbrella',
'handbag',
'tie',
'suitcase',
'frisbee',
'skis',
'snowboard',
'sports ball',
'kite',
'baseball bat',
'baseball glove',
'skateboard',
'surfboard',
'tennis racket',
'bottle',
'wine glass',
'cup',
'fork',
'knife',
'spoon',
'bowl',
'banana',
'apple',
'sandwich',
'orange',
'broccoli',
'carrot',
'hot dog',
'pizza',
'donut',
'cake',
'chair',
'sofa',
'pottedplant',
'bed',
'diningtable',
'toilet',
'tvmonitor',
'laptop',
'mouse',
'remote',
'keyboard',
'cell phone',
'microwave',
'oven',
'toaster',
'sink',
'refrigerator',
'book',
'clock',
'vase',
'scissors',
'teddy bear',
'hair drier',
'toothbrush'],anchor,objThreshold=0.5, confThreshold=0.8, nmsThreshold=0.2)  #objThreshold-对象置信度 confThreshold-种类置信度 nmsThreshold-nms iou
    cap = cv2.VideoCapture(0)
    while True:
        _,img = cap.read() 
        data = model.run(img)
        for i in data:
            print(i)
            if i['id']==0:
                cv2.rectangle(img, (i['position'][0],i['position'][1] ), (i['position'][2], i['position'][3]), (255,0,0), thickness=2)
            else:
                cv2.rectangle(img, (i['position'][0],i['position'][1] ), (i['position'][2], i['position'][3]), (0,0,255), thickness=2)
        cv2.imshow('OpenCV',img)
        if cv2.waitKey(25) == ord('q'):
            break
    cv2.waitKey(0)
    cv2.destroyAllWindows()
