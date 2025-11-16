from functools import wraps
from flask import redirect, url_for
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('web.login'))

        user_role = getattr(current_user, 'role', None)
        if user_role == 'admin':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('web.home'))
    return decorated_function