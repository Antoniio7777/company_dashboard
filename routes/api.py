from flask import request, jsonify, Blueprint, session
from models import User
from app import db, bcrypt
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required
from decorators import admin_required
import secrets
import string

api_bp = Blueprint('api', __name__, url_prefix='/api')

#Logging in user (returns json success and message)
@api_bp.route('/checklogin', methods=['POST'])
def checklogin():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        session.clear()
        login_user(user)
        return jsonify({"success": True, "message": "Login successful"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid username or password!"}), 401

# Changing password (returns json success and message) (login required)
@api_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    old_password = (data.get('old_password') or '').strip()
    new_password = (data.get('new_password') or '').strip()

    if not bcrypt.check_password_hash(current_user.password, old_password):
        return jsonify({"success": False, "message": "Invalid old password"}), 403

    if new_password == old_password:
        return jsonify({"success": False, "message": "New password is same as old"}), 400

    if len(new_password) < 4:
        return jsonify({"success": False, "message": "Password too short"}), 400

    current_user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Password changed"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}), 500


#=================
#Admin panel APIs
#=================

#Adding new user (returns json success and message) (admin required)
@api_bp.route('/adduser', methods=['POST'])
@admin_required
def adduser():
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}), 400

    username = (data.get('username') or '').strip().lower()
    password = (data.get('password') or '').strip()
    role = (data.get('role') or '')


    if User.query.filter_by(username=username).first():
        return jsonify({"success": False, "message": "User already exists"}), 409

    if len(password) < 4:
        return jsonify({"success": False, "message": "Password too short"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password, role=role)

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

#Getting a list of user (returns json success + users list or message)
@api_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        users = User.query.all()
        users_list=[{"id": user.id, "username": user.username, "role": user.role} for user in users]
        return jsonify({"success": True, "users": users_list}), 200
    except Exception:
        return jsonify({"success": False, "message": "Server error"}), 500


#Deleting user (returns json success + message)
@api_bp.route('/users/<int:uid>/delete', methods=['DELETE'])
@admin_required
def delete_user(uid):
    user = User.query.get(uid)
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if current_user == user:
        return jsonify({"success": False, "message": "Cannot delete yourself"}), 400
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User deleted"}),200
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}),500


#Changing user role (returns json success + message)
@api_bp.route('/users/<int:uid>/role', methods=['PATCH'])
@admin_required
def change_role(uid):
    data = request.get_json(silent=True)
    if not data or not isinstance(data, dict):
        return jsonify({"success": False, "message": "Invalid JSON"}),400

    new_role = data.get('role')
    user = User.query.get(uid)

    if not user:
        return jsonify({"success": False, "message": "User not found"}),404

    if new_role == user.role:
        return jsonify({"success": False, "message": "Cannot change to the same role"}),400

    user.role = new_role
    try:
        db.session.commit()
        return jsonify({"success": True, "message": "Role changed"}),200
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}),500


#Resetting user password (returns json success + new password or message)
@api_bp.route('/users/<int:uid>/reset_password', methods=['PATCH'])
@admin_required
def reset_password(uid):

    user = User.query.get(uid)

    if not user:
        return jsonify({"success": False, "message": "User not found"}),404

    new_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(8))

    user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    try:
        db.session.commit()
        return jsonify({"success": True, "password": new_password}),200
    except Exception:
        db.session.rollback()
        return jsonify({"success": False, "message": "Server error"}),500
