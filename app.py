from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config_by_name

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app(config_name: str = os.getenv('FLASK_ENV')) -> Flask:
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_by_name[config_name])
    Talisman(app, content_security_policy=app.config.get("TALISMAN_CONTENT_SECURITY_POLICY"))
    CSRFProtect(app)
    db.init_app(app)
    login_manager.init_app(app)

    from models import User

    from routes.api import api_bp
    from routes.web import web_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(web_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    login_manager.login_view='web.login'

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({"success": False, "message": "Server error"}), 500

    migrate = Migrate(app, db)
    return app