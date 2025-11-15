from flask import request, jsonify, Response, Blueprint
from werkzeug.exceptions import BadRequest
from models import User
from app import db, bcrypt
from flask_login import login_user, logout_user


api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/checklogin', methods=['POST'])
def checklogin() -> Response:
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
        except BadRequest:
            return jsonify({"success": False, "message": "Invalid JSON!"})

        user = User.query.filter_by(user=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"success": True, "message": "Login successful"})
        else:
            return jsonify({"success": False, "message": "Invalid username or password!"})

@api_bp.route('/adduser', methods=['POST'])
def adduser() -> Response:
        try:
            data = request.get_json()
            username = data.get('user').strip()
            password = data.get('password').strip()
            can_modify = data.get('canModify')
            is_admin = data.get('admin')
        except BadRequest:
            return jsonify({"success": False, "message": "Invalid JSON!"})

        if not username or not password:
            return jsonify({"success": False, "message": "Enter user and password"})

        if User.query.filter_by(user=username).first():
            return jsonify({"success": False, "message": "User already exist!"})

        if len(password)<4:
            return jsonify({"success": False, "message": "Password too short!"})

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(user=username, password=hashed_password, can_modify=can_modify, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        return jsonify({"success": True, "message": "User added"})
