from flask import Blueprint, render_template, request, redirect, session
from config import admin_collection
from werkzeug.security import check_password_hash
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    return redirect('/login')

@auth_bp.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    admin = admin_collection.find_one({'username': username})
    
    if admin and check_password_hash(admin['password'], password):
        session['username'] = admin['username']
        return redirect('/trainer')
    else:
        return render_template('login.html', error="Invalid credentials")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
