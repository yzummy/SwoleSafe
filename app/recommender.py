import flask
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_cors import CORS

import json

app = Flask(__name__)

api = Api(app)
CORS(app)


@app.route('/recommend', methods = ['GET', 'POST'])
def bicepCurl():

if __name__ == '__main__':
        keypoints = []
            np_keypoints = np.array([])
                app.secret_key = 'super secret key'
                    app.config['SESSION_TYPE'] = 'filesystem'
                        app.run(port='5002')