from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.trainer_routes import trainer_bp
# from routes.subject_route import subject_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(trainer_bp)
# app.register_blueprint(subject_bp)

if __name__ == '__main__':
    app.run(debug=True)
