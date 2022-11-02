
from app import app
from flask_cors import CORS,cross_origin

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/api/getdata', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type'])
def get_todos():
   
    return "Get Request API Check"