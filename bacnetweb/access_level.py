from functools import wraps

from flask import url_for, redirect, flash
from flask_login import current_user

from bacnetweb.models import User, Schedule, Alarm


def requires_access_level():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Log-in with the proper user to access this endpoint.', 'danger')
                return redirect(url_for('auth.login'))

            user = User.query.filter_by(usr=current_user.usr).first()
            if not user.allowed():
                flash('You do not have access to that page. Sorry!', 'danger')
                return redirect(url_for('users.profile'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def requires_access_alarm(func):
    @wraps(func)
    def wraper(alarm_id, *args, **kwargs):
        alarm = Alarm.query.filter_by(id=alarm_id).first()

        if current_user.allowed():
            return func(alarm_id, *args, **kwargs)
        if alarm.id_user != current_user.id:
            flash('You do not have access to that page. Sorry!', 'danger')
            return redirect(url_for('main.index'))
        return func(alarm_id, *args, **kwargs)

    return wraper


def requires_access_schedule(func):
    @wraps(func)
    def wraper(schedule_id, *args, **kwargs):
        sch = Schedule.query.filter_by(id=current_user.schedule_id).first()
        if current_user.allowed():
            return func(schedule_id, *args, **kwargs)

        if sch.id_user != current_user.id:
            flash('You do not have access to that page. Sorry!', 'danger')
            return redirect(url_for('main.index'))
        return func(schedule_id, *args, **kwargs)

    return wraper
