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
from convertData import convert
from realTimeEvaluate import _bicep_curl, _front_raise, _squat, _push_up
import numpy as np
import json

app = Flask(__name__)

api = Api(app)
CORS(app)


           
@app.route('/bicepCurl', methods = ['GET', 'POST'])
def bicepCurl():
    if flask.request.method == 'GET':
        return jsonify({})
    if flask.request.method == 'POST':
        global np_keypoints
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
            warns = ["You are doing great!", "Keep up!"]
            if tooMuchRotation:            
                result[0] = 1
                warns[0] = "Your upper arm shows too much rotation! Try to hold the upper arm still!"
                print("Your upper arm shows too much rotation! Try to hold the upper arm still!")
            if notHighEnough:
                result[1] = 1
                warns[1] = "Curl higher!!!"
                print("Curl higher!!!")
            return jsonify({'e1':result[0], 'e2':result[1], 'warn0':warns[0], 'warn1':warns[1]})
        return jsonify({})
    return jsonify({})
    

@app.route('/frontRaise', methods = ['GET', 'POST'])
def frontRaise():
    if flask.request.method == 'GET':
        return jsonify({})
    if flask.request.method == 'POST':
        global np_keypoints
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
            tooMuchRotation, notHighEnough = _front_raise(np_keypoints)
            result = [0,0]
            warns = ["You are doing great!", "Keep up!"]
            if tooMuchRotation:            
                result[0] = 1
                warns[0] = "Too much torso movement! Stay still! "
                print("Too much torso movement! Stay still! ")
            if notHighEnough:
                result[1] = 1
                warns[1] = "Raise higher! You can do it!"
                print("Raise higher! You can do it!")
            return jsonify({'e1':result[0], 'e2':result[1], 'warn0':warns[0], 'warn1':warns[1]})
        return jsonify({})
    return jsonify({})
    
    
    
@app.route('/deepSquat', methods = ['GET', 'POST'])
def deepSquat():
    if flask.request.method == 'GET':
        return jsonify({})
    if flask.request.method == 'POST':
        global np_keypoints
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
            notParallel, tooSeparate = _squat(np_keypoints)
            result = [0,0]
            warns = ["You are doing great!", "Keep up!"]
            if notParallel:            
                result[0] = 1
                warns[0] = "Squat deeper! Not low enough! "
                print("Squat deeper! Not low enough! ")
            if tooSeparate:
                result[1] = 1
                warns[1] = "Match your heels with shoulder-width!"
                print("Match your heels with shoulder-width!")
            return jsonify({'e1':result[0], 'e2':result[1], 'warn0':warns[0], 'warn1':warns[1]})
        return jsonify({})
    return jsonify({})

    
@app.route('/pushUp', methods = ['GET', 'POST'])
def pushUp():
    if flask.request.method == 'GET':
        return jsonify({})
    if flask.request.method == 'POST':
        global np_keypoints
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
            notStraight, notLowEnough = _squat(np_keypoints)
            result = [0,0]
            warns = ["You are doing great!", "Keep up!"]
            if notStraight:            
                result[0] = 1
                warns[0] = "Keep your body in a straight line!"
                print("Keep your body in a straight line! ")
            if notLowEnough:
                result[1] = 1
                warns[1] = "Get lower! You can do it! "
                print("Get lower! You can do it!")
            return jsonify({'e1':result[0], 'e2':result[1], 'warn0':warns[0], 'warn1':warns[1]})
        return jsonify({})
    return jsonify({})

if __name__ == '__main__':
    keypoints = []
    np_keypoints = np.array([])
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port='5002')
     