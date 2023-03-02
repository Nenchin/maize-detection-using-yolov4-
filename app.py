# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:57:35 2023

@author: Nenchin
"""

import sys
import cv2
import argparse
import random
import time
from flask import Flask, render_template, Response

app = Flask(__name__)

@app.route("/video_feed")
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag"""
    return Response(YOLOv4().run_inference(), mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/")
def index():
    """Video streaming home page."""
    return render_template("index.html")


class YOLOv4:

    def __init__(self):
        """ Method called when object of this class is created. """


        self.initialize_network()

    def initialize_network(self):
        """ Method to initialize and load the model."""

        self.net = cv2.dnn_DetectionModel("yolov4test-obj.cfg", "yolov4-obj_last.weights")
        
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

            
        self.net.setInputSize(416, 416)
        self.net.setInputScale(1.0 / 255)
        self.net.setInputSwapRB(True)
        with open("obj.names", 'rt') as f:
            self.names = f.read().rstrip('\n').split('\n')
            
            
    def run_inference(self):

        source = cv2.VideoCapture(0)

        while(source.isOpened()):
            ret, frame = source.read()
            if ret:
                timer = time.time()
                classes, confidences, boxes = self.net.detect(frame, confThreshold=0.1, nmsThreshold=0.4)
                print('[Info] Time Taken: {} | FPS: {}'.format(time.time() - timer, 1/(time.time() - timer)), end='\r')
                
                if(not len(classes) == 0):
                    for classId, confidence, box in zip(classes.flatten(), confidences.flatten(), boxes):
                        label = '%s: %.2f' % (self.names[classId], confidence)
                        left, top, width, height = box
                        b = random.randint(0, 255)
                        g = random.randint(0, 255)
                        r = random.randint(0, 255)
                        cv2.rectangle(frame, box, color=(b, g, r), thickness=2)
                        cv2.rectangle(frame, (left, top), (left + len(label) * 20, top - 30), (b, g, r), cv2.FILLED)
                        cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_COMPLEX, 1, (255 - b, 255 - g, 255 - r), 1, cv2.LINE_AA)

                ret, buffer = cv2.imencode(".jpg", frame)
                frame = buffer.tobytes()
                yield (b"--frame\r\n"
                       b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n") #concat frame one by one and show result
                
                
if __name__=="__main__":
    yolo = YOLOv4.__new__(YOLOv4)
    yolo.__init__()
    app.run(port=2222, debug=True)
