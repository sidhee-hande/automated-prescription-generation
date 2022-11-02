from flask import Flask
from flask import Flask,request, jsonify
from flask_cors import CORS,cross_origin

app = Flask(__name__)

CORS(app,resources={r"/api": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

from app import routes