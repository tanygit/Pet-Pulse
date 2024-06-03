from flask import Flask
from config import Config
from routes import main_blueprint
from flask_socketio import SocketIO
import os

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object(Config)

# Configure the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'petpulse_tanmay/petpulse/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Initialize SocketIO
socketio = SocketIO(app)

# Register Blueprints
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    # Run the app with SocketIO
    socketio.run(app, debug=True)
