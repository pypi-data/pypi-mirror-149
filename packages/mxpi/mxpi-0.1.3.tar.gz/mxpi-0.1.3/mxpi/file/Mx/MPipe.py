#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import argparse
from ctypes import c_void_p
from pyexpat import model
import cv2 as cv
import numpy as np
import mediapipe as mp
import os,time
import shutil,requests
import urllib.request
import math

'''
#人体姿态检测
#参数(模型复杂度[0,1,2],检测置信度,跟踪置信度,分段阈值,检测范围)
    hands=pose(0,0.7,0.5,0.5,0.5)                        
    cap = cv.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        dk=hands.run(frame)
        print(dk)
        for i in dk:
            cv.circle(frame, (i[0],i[1]), 3, (0, 255, 0), -1)

        cv.imshow("",frame)
        if cv.waitKey(100) & 0xff == ord('q'):
                break
    cv.waitKey(0)
    cv.destroyAllWindows()
'''
class pose():
    def __init__(self,model_complexity,min_detection_confidence,min_tracking_confidence,segmentation_score_th,visibility_th):
        self._download_oss_pose_landmark_model(model_complexity)
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.segmentation_score_th = segmentation_score_th
        self.visibility_th=visibility_th
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
    def run(self,cv_img):
        image = cv_img
        debug_image = copy.deepcopy(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.pose.process(image)
        if results.pose_landmarks is not None:
            #人体矩形框
            rect = self.calc_bounding_rect(debug_image, results.pose_landmarks)
            dlandmark = self.dlandmarks(debug_image,results.pose_landmarks,self.visibility_th)
            return {'rect':rect,'dlandmark':dlandmark}
        else:
            return None
    
    def calc_bounding_rect(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point = [np.array((landmark_x, landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)
        x, y, w, h = cv.boundingRect(landmark_array)
        return [x, y, w, h]

    def dlandmarks(self,image,landmarks,visibility_th):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        for index, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_z = landmark.z
            landmark_point.append([landmark_x, landmark_y,landmark_z])
        return landmark_point
    
    def _download_oss_pose_landmark_model(self,model_complexity):
        """Downloads the pose landmark lite/heavy model from the YuanYunQiang CodeGit repo if it doesn't exist in the package."""
        if model_complexity == 0:
            self.download_oss_model('modules/pose_landmark/pose_landmark_lite.tflite','pose_landmark_lite.tflite')
        elif model_complexity == 2:
            self.download_oss_model('modules/pose_landmark/pose_landmark_heavy.tflite','pose_landmark_heavy.tflite')
    
    def download_oss_model(self,model_path: str,name):
        """Downloads the oss model from the MediaPipe CodeGit repo if it doesn't exist in the package."""
        url = 'https://gitcode.net/q924257/mediapipe-title/raw/master/'+name
        r = requests.get(url,stream=True) 
        size = r.headers.get('Content-Length')
        mp_root_path = mp.__path__[0]
        model_abspath = os.path.join(mp_root_path, model_path)
        if os.path.exists(model_abspath):
            return
        print ("Downing "+name+" with GitCode")
        file = open(model_abspath,'wb')
        s=0
        P2=0
        print('Model Size:'+size+'byte')
        for i in r.iter_content(chunk_size=1024):
            file.write(i)
            s += 1024
            P1=int(s/int(size)*100)
            if P1!=P2:
                print('Down:'+str(int(s/int(size)*100))+' %'+'  '+str(s)+'/'+size)
                P2=int(s/int(size)*100)
        print('Downing end!')


'''
手部识别，参数(模型复杂度[0 or 1],识别手的数量,检测置信度,跟踪置信度)
    hand=hands(0,2,0.7,0.5)                        
    cap = cv.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        dk=hand.run(frame)
        print(dk)
        for s in dk:
            for xy in s['dlandmark']:
                cv.circle(frame, xy, 3, (0, 255, 0), -1)
        cv.imshow('',frame)
        if cv.waitKey(100) & 0xff == ord('q'):
                break
    cv.waitKey(0)
    cv.destroyAllWindows()'''
class hands():
    def __init__(self,model_complexity,max_num_hands,min_detection_confidence,min_tracking_confidence):
        self.model_complexity = model_complexity
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )
    
    def run(self,cv_img):
        image = cv_img
        debug_image = copy.deepcopy(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.hands.process(image)
        hf=[]
        if results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                  results.multi_handedness):
                # 手的重心计算
                cx, cy = self.calc_palm_moment(debug_image, hand_landmarks)
                # 手的外接矩形计算
                rect = self.calc_bounding_rect(debug_image, hand_landmarks)
                # 手的个关键点
                dlandmark = self.dlandmarks(debug_image,hand_landmarks,handedness)
                hf.append({'center':(cx,cy),'rect':rect,'dlandmark':dlandmark[0],'right_left':dlandmark[1]})
        return hf

    def calc_palm_moment(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        palm_array = np.empty((0, 2), int)
        for index, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point = [np.array((landmark_x, landmark_y))]
            if index == 0:  # 手首1
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 1:  # 手首2
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 5:  # 人差指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 9:  # 中指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 13:  # 薬指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
            if index == 17:  # 小指：付け根
                palm_array = np.append(palm_array, landmark_point, axis=0)
        M = cv.moments(palm_array)
        cx, cy = 0, 0
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        return cx, cy

    def calc_bounding_rect(self, image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point = [np.array((landmark_x, landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)
        x, y, w, h = cv.boundingRect(landmark_array)
        return [x, y, w, h]

    def dlandmarks(self,image, landmarks, handedness):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        for index, landmark in enumerate(landmarks.landmark):
            if landmark.visibility < 0 or landmark.presence < 0:
                continue
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point.append((landmark_x, landmark_y))
        return landmark_point,handedness.classification[0].label[0]

'''
人脸468个关键点检测  参数(最大识别人脸数,检测置信度,跟踪置信度)
    face=face_mesh(2,0.7,0.5)                        
    cap = cv.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        dk=face.run(frame)
        print(dk)
        if cv.waitKey(100) & 0xff == ord('q'):
                break
    cv.waitKey(0)
    cv.destroyAllWindows()
'''
class face_mesh():
    def __init__(self,max_num_faces,min_detection_confidence,min_tracking_confidence):
        self.max_num_faces = max_num_faces
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.f=[]
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=self.max_num_faces,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence,
        )

    def run(self,cv_img):
        image = cv_img  # ミラー表示
        debug_image = copy.deepcopy(image)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.face_mesh.process(image)
        self.f_rect=[]
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                brect = self.calc_bounding_rect(debug_image, face_landmarks)
                dlandmark=self.dlandmarks(debug_image,face_landmarks)
                self.f_rect.append({'face_rect':brect,'landmark_point':dlandmark})
        return self.f_rect

    def calc_bounding_rect(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_array = np.empty((0, 2), int)
        for _, landmark in enumerate(landmarks.landmark):
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point = [np.array((landmark_x, landmark_y))]
            landmark_array = np.append(landmark_array, landmark_point, axis=0)
        x, y, w, h = cv.boundingRect(landmark_array)
        return [x, y, w, h]

    def dlandmarks(self,image, landmarks):
        image_width, image_height = image.shape[1], image.shape[0]
        landmark_point = []
        for index, landmark in enumerate(landmarks.landmark):
            if landmark.visibility < 0 or landmark.presence < 0:
                continue
            landmark_x = min(int(landmark.x * image_width), image_width - 1)
            landmark_y = min(int(landmark.y * image_height), image_height - 1)
            landmark_point.append((landmark_x, landmark_y))
        return landmark_point

'''
 #人脸关键点5检测
 参数：最小置信度
    face=face_detection(0.7)                        
    cap = cv.VideoCapture(0)
    while 1:
        ret, frame = cap.read()
        print(face.run(frame))
        if cv.waitKey(100) & 0xff == ord('q'):
                break
    cv.waitKey(0)
    cv.destroyAllWindows()
'''
class face_detection():
    def __init__(self,min_detection_confidence):
        self.model_selection = 0
        self.min_detection_confidence =min_detection_confidence
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            min_detection_confidence=self.min_detection_confidence,
        )

    def run(self,cv_img):
        image = cv_img
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.face_detection.process(cv_img)
        face=[]
        if results.detections is not None:
            for detection in results.detections:
                data =self.draw_detection(image,detection) 
                face.append(data)
        return face
    def draw_detection(self, image, detection):
        image_width, image_height = image.shape[1], image.shape[0]
        bbox = detection.location_data.relative_bounding_box
        bbox.xmin = int(bbox.xmin * image_width)
        bbox.ymin = int(bbox.ymin * image_height)
        bbox.width = int(bbox.width * image_width)
        bbox.height = int(bbox.height * image_height)


        # 位置：右目
        keypoint0 = detection.location_data.relative_keypoints[0]
        keypoint0.x = int(keypoint0.x * image_width)
        keypoint0.y = int(keypoint0.y * image_height)


        # 位置：左目
        keypoint1 = detection.location_data.relative_keypoints[1]
        keypoint1.x = int(keypoint1.x * image_width)
        keypoint1.y = int(keypoint1.y * image_height)


        # 位置：鼻
        keypoint2 = detection.location_data.relative_keypoints[2]
        keypoint2.x = int(keypoint2.x * image_width)
        keypoint2.y = int(keypoint2.y * image_height)


        # 位置：口
        keypoint3 = detection.location_data.relative_keypoints[3]
        keypoint3.x = int(keypoint3.x * image_width)
        keypoint3.y = int(keypoint3.y * image_height)

        # 位置：右耳
        keypoint4 = detection.location_data.relative_keypoints[4]
        keypoint4.x = int(keypoint4.x * image_width)
        keypoint4.y = int(keypoint4.y * image_height)

        # 位置：左耳
        keypoint5 = detection.location_data.relative_keypoints[5]
        keypoint5.x = int(keypoint5.x * image_width)
        keypoint5.y = int(keypoint5.y * image_height)

        data={'id':detection.label_id[0],
            'score':round(detection.score[0], 3),
            'rect':[int(bbox.xmin),int(bbox.ymin),int(bbox.width),int(bbox.height)],
            'right_eye':(int(keypoint0.x),int(keypoint0.y)),
            'left_eye':(int(keypoint1.x),int(keypoint1.y)),
            'nose':(int(keypoint2.x),int(keypoint2.y)),
            'mouth':(int(keypoint3.x),int(keypoint3.y)),
            'right_ear':(int(keypoint4.x),int(keypoint4.y)),
            'left_ear':(int(keypoint5.x),int(keypoint5.y)),
            }
        return data
