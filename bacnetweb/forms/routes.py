from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Email, EqualTo, DataRequired, ValidationError

from bacnetweb.models import User


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Password Repeat', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(usr=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class UpdateForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Current Password', validators=[DataRequired()])
    password_new = PasswordField('New Password', validators=[])
    password_repeat = PasswordField('Password Repeat', validators=[EqualTo('password_new')])
    submit = SubmitField('Update')


class ResetPassForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')


class ChangePassForm(FlaskForm):
    password_new = PasswordField('New Password', validators=[])
    password_repeat = PasswordField('Password Repeat', validators=[EqualTo('password_new')])
    submit = SubmitField('Reset Password')


class AdminSignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Password Repeat', validators=[DataRequired(), EqualTo('password')])
    admin = BooleanField('Administrator')
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(usr=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


class AdminUserForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password_new = PasswordField('New Password', validators=[])
    password_repeat = PasswordField('Password Repeat', validators=[EqualTo('password_new')])
    admin = BooleanField('Administrator')
    submit = SubmitField('Update')


class SchedulesForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('description', validators=[DataRequired()])
    submit = SubmitField('Register')


class SchedulesRegisterForm(FlaskForm):
    id_user = StringField('User')
    object_identifier = StringField('Object ID', validators=[DataRequired()])
    object_name = StringField('Object Name', validators=[DataRequired()])
    object_type = StringField('Object Type', validators=[DataRequired()])
    present_value = StringField('Present Value', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    effective_period = StringField('Effective Period', validators=[DataRequired()])
    exception_schedule = StringField('Exception Sch', validators=[DataRequired()])
    list_of_object_property_references = StringField('Properties', validators=[DataRequired()])
    priority_for_writing = StringField('Priority For Writing', validators=[DataRequired()])
    status_flags = StringField('Status Flags', validators=[DataRequired()])
    reliability = StringField('Reliability', validators=[DataRequired()])
    out_of_service = BooleanField('Out Of Service')
    submit = SubmitField('Register')


class DailyScheduleRegisterForm(FlaskForm):
    day = SelectField('Day', choices=[('Monday', 'Monday'),
                                      ('Tuesday', 'Tuesday'),
                                      ('Wednesday', 'Wednesday'),
                                      ('Thursday', 'Thursday'),
                                      ('Friday', 'Friday'),
                                      ('Saturday', 'Saturday'),
                                      ('Sunday', 'Sunday')])
    initial_time = StringField('Initial Time', validators=[DataRequired()])
    final_time = StringField('Final Time', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_value(self, value):
        print(value.data.isdigit())
        if not value.data.isdigit():
            raise ValidationError('Format value not correct, insert digit.')


class SpecialScheduleRegisterForm(FlaskForm):
    day = StringField('Day', validators=[DataRequired()])
    initial_time = StringField('Initial Time', validators=[DataRequired()])
    final_time = StringField('Final Time', validators=[DataRequired()])
    value = StringField('Value', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_value(self, value):
        print(value.data.isdigit())
        if not value.data.isdigit():
            raise ValidationError('Format value not correct, insert digit.')


class AlarmsRegisterForm(FlaskForm):
    state = SelectField('State', choices=[('Active', 'Active'),
                                          ('Inactive', 'Inactive')])
    event = SelectField('Event', choices=[('Normal', 'Normal'),
                                          ('Offnormal', 'Offnormal'),
                                          ('Fault', 'Fault')])
    source = StringField('Source', validators=[DataRequired()])
    source_description = StringField('Source Description', validators=[DataRequired()])
    alarm_text = StringField('Alarm Text', validators=[DataRequired()])
    triggered_time = StringField('Triggered Time', validators=[DataRequired()])
    id_user = StringField('User')
    submit = SubmitField('Register')
