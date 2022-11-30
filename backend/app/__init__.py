from quart import Quart
from quart import Quart,request, jsonify
from quart_cors import cors

app = Quart(__name__)

# CORS(app,resources={r"/api": {"origins": "*"}})
app = cors(app, allow_origin="*")
app.config['CORS_HEADERS'] = 'Content-Type'

from app import routes