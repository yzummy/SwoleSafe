import flask
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import argmax, unique
import json
from convertData import convert
from realTimeEvaluate import _bicep_curl
import numpy as np

app = Flask(__name__)

api = Api(app)
CORS(app)


           
@app.route('/poseup', methods = ['GET', 'POST'])
def poseUp():
    print("You are cropping an image\n")

    if flask.request.method == 'GET':
        return jsonify({})
    if flask.request.method == 'POST':
        print("hello world")
        global np_keypoints
        #print('request.files', json.loads(request.files['pose'].read()))
        pose = json.loads(request.files['pose'].read())
        keypoints.append(pose)
        if len(keypoints) == 10:
            np_keypoints = convert(keypoints)
        if len(keypoints) > 10:
            k = convert([pose])
            print(np_keypoints.shape, k.shape)
            np_keypoints = np.concatenate((np_keypoints, k), axis=0)
        print(np_keypoints.shape)
        if np_keypoints.shape[0] % 10 == 0:
            tooMuchRotation, notHighEnough = _bicep_curl(np_keypoints)
            result = [0,0]
            if tooMuchRotation:            
                result[0] = 1
                print("Your upper arm shows too much rotation! Try hold the upper arm still!")
            if notHighEnough:
                result[1] = 1
                print("Curl higher!!!")
            return jsonify({'tooMuchRotation':result[0], 'notHighEnough':result[1]})
        return jsonify({})
    return jsonify({})



if __name__ == '__main__':
    keypoints = []
    np_keypoints = np.array([])
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port='5002')
     