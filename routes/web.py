from flask import render_template, Response, Blueprint, redirect, url_for, session
from flask_wtf.csrf import generate_csrf
from flask_login import login_required, logout_user
from decorators import admin_required

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET', 'POST'])
def login() -> Response:
    csrf_token = generate_csrf()
    return render_template('login.html', csrf_token=csrf_token)

@web_bp.route('/home')
@login_required
def home() -> Response:
    csrf_token = generate_csrf()
    return render_template('home.html', csrf_token=csrf_token)

@web_bp.route('/logout', methods=['POST'])
@login_required
def logout() -> Response:
    logout_user()
    session.clear()
    return redirect(url_for('web.login'))

@web_bp.route('/change_password', methods=['POST'])
@login_required
def change_password() -> Response:
    csrf_token = generate_csrf()
    return render_template('change_password.html', csrf_token=csrf_token)

@web_bp.route('/adminpanel', methods=['POST', 'GET'])
@admin_required
def adminpanel() -> Response:
    csrf_token = generate_csrf()
    return render_template('admin_panel.html', csrf_token=csrf_token)