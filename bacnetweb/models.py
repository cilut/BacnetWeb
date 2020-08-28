from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from bacnetweb import login_manager, admin, db
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    usr = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def allowed(self):
        return self.admin


class Schedule(UserMixin, db.Model):
    __tablename__ = "schedules"
    id = db.Column(db.Integer, primary_key=True)
    object_identifier = db.Column(db.String, nullable=False)
    object_name = db.Column(db.String, nullable=False)
    object_type = db.Column(db.String, nullable=False)
    present_value = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    effective_period = db.Column(db.String, nullable=False)
    exception_schedule = db.Column(db.String, nullable=False)
    list_of_object_property_references = db.Column(db.String, nullable=False)
    priority_for_writing = db.Column(db.String, nullable=False)
    status_flags = db.Column(db.String, nullable=False)
    reliability = db.Column(db.String, nullable=False)
    out_of_service = db.Column(db.Boolean, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)


class DailySchedule(db.Model):
    __tablename__ = "dailyschedules"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    initial_time = db.Column(db.String, nullable=False)
    final_time = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    object_id = db.Column(db.Integer, nullable=False)


class Alarm(UserMixin, db.Model):
    __tablename__ = "alarms"
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String, nullable=False)
    event = db.Column(db.String, nullable=False)
    source = db.Column(db.String, nullable=False)
    source_description = db.Column(db.String, nullable=False)
    alarm_text = db.Column(db.String, nullable=False)
    triggered_time = db.Column(db.String, nullable=False)
    id_user = db.Column(db.Integer, nullable=False)


class MyModelView(ModelView):
    column_labels = dict(usr='Username', email='Email', admin='Administrator')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.admin


admin.add_view(MyModelView(User, db.session))
