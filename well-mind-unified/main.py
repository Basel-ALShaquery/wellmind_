import os
import sys
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.mood import mood_bp
from src.models.mood import Mood, TestResult

# Ensure "database" folder exists
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, 'database')
os.makedirs(DB_FOLDER, exist_ok=True)  # Creates folder if it doesn't exist

# Path to the SQLite database file
DB_PATH = os.path.join(DB_FOLDER, "app.db")

# Path to the built frontend (React/Vite)
DIST_PATH = os.path.join(BASE_DIR, "dist")

# Initialize Flask app
app = Flask(__name__, static_folder=DIST_PATH, template_folder=DIST_PATH)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Enable CORS
CORS(app)

# Register Blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(mood_bp, url_prefix='/api')

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# Serve frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(DIST_PATH, path)):
        return send_from_directory(DIST_PATH, path)
    else:
        return send_from_directory(DIST_PATH, "index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
