from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.trainer_routes import trainer_bp
from routes.subject_routes import subject_bp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(trainer_bp)
app.register_blueprint(subject_bp)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render looks for this
    app.run(host='0.0.0.0', port=port, debug=True)
