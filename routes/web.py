from flask import render_template, Response, Blueprint
from flask_wtf.csrf import generate_csrf
from flask_login import login_required

web_bp = Blueprint('web', '__name__')

@web_bp.route('/', methods=['GET', 'POST'])
def login() -> Response:
    csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)

@web_bp.route('/home')
@login_required
def home() -> Response:
    return "<h1>Welcome to the ToDo List!</h1>"

@web_bp.route('/dev', methods=['GET'])
def dev():
    csrf_token = generate_csrf()
    return render_template('createuser.html', csrf_token=csrf_token)