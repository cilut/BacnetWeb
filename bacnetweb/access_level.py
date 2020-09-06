from functools import wraps

from flask import url_for, redirect, flash
from flask_login import current_user

from bacnetweb.models import User


def requires_access_level():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Log-in with the proper user to access this endpoint.', 'danger')
                return redirect(url_for('auth.auth'))

            user = User.query.filter_by(usr=current_user.usr).first()
            if not user.allowed():
                flash('You do not have access to that page. Sorry!', 'danger')
                return redirect(url_for('users.profile'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
