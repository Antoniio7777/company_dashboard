from flask import request, jsonify, Blueprint, session
from models import User
from app import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required
from decorators import admin_required

api_bp = Blueprint('api', __name__, url_prefix='/api')

#Logging in user (returns json success and message)
@api_bp.route('/checklogin', methods=['POST'])
def checklogin():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()
    user = User.query.filter_by(user=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session.clear()
        login_user(user)
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid login or password!"}), 401


#Adding new user (returns json success and message) (admin required)
@api_bp.route('/adduser', methods=['POST'])
@login_required
@admin_required
def adduser():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()
    role = (data.get('role') or '')


    if User.query.filter_by(user=username).first():
        return jsonify({"success": False, "message": "User already exists"}), 409

    if len(password) < 4:
        return jsonify({"success": False, "message": "Password too short"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(user=username, password=hashed_password, role=role)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User added"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "User already exists"}), 409
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500


#Changing password (returns json success and message) (login required)
@api_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    old_password = (data.get('old_password') or '').strip()
    new_password = (data.get('new_password') or '').strip()

    user = User.query.filter_by(user=current_user.user).first()

    if not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({"success": False, "message": "Invalid old password"}), 403

    if new_password == old_password:
        return jsonify({"success": False, "message": "New password is same as old"}), 400

    if len(new_password) < 4:
        return jsonify({"success": False, "message": "Password too short"}), 400

    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Password changed"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server errro"}), 500


#Getting a list of user (returns json success + users list or message)
@api_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    try:
        users = User.query.all()
        users_list = [{"id": u.id, "user": u.user, "role": u.role} for u in users]
        return jsonify({"success": True, "users": users_list}), 200
    except Exception:
        return jsonify({"success": False, "message": "Server error"}), 500