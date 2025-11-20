from flask import render_template, Response, Blueprint, redirect, url_for, session
from flask_login import login_required, logout_user
from decorators import admin_required

web_bp = Blueprint('web', __name__)

@web_bp.route('/', methods=['GET'])
def login() -> Response:
    return render_template('login.html')

@web_bp.route('/home')
@login_required
def home() -> Response:
    return render_template('home.html')

@web_bp.route('/logout', methods=['POST'])
@login_required
def logout() -> Response:
    logout_user()
    session.clear()
    return redirect(url_for('web.login'))

@web_bp.route('/change_password', methods=['GET'])
@login_required
def change_password() -> Response:
    return render_template('change_password.html')

@web_bp.route('/adminpanel', methods=['GET'])
@admin_required
def adminpanel() -> Response:
    return render_template('admin_panel.html')

@web_bp.route('/dev')
def dev() -> Response:
    raise Exception("ERROR")