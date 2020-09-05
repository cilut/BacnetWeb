import re

from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from bacnetweb import db
from bacnetweb.access_level import requires_access_level
from bacnetweb.forms.routes import AdminUserForm, AdminSignupForm, SchedulesRegisterForm, AlarmsRegisterForm
from bacnetweb.models import User, Schedule, DailySchedule, Alarm

admin = Blueprint('admin', __name__)


@admin.route('/admin/users', methods=['GET', 'POST'])
@requires_access_level()
def users():
    all_users = User.query.all()
    return render_template('admin/all_users.html', users=all_users)


@admin.route('/admin/users/<user_id>', methods=['GET', 'POST'])
@requires_access_level()
def update_user(user_id):
    form = AdminUserForm()
    user = User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.password = generate_password_hash(form.password_new.data, "sha256")
        user.email = form.email.data
        user.admin = form.admin.data
        db.session.add(user)
        db.session.commit()
        flash(f'Account updated for {user.usr}', 'success')
        return redirect(url_for("admin.users"))
    return render_template('admin/user.html', title='Account', form=form, user=user)


@admin.route("/admin/users/signup", methods=['GET', 'POST'])
@requires_access_level()
def register_user():
    form = AdminSignupForm()
    if form.validate_on_submit():
        usr = User(usr=form.username.data, password=generate_password_hash(form.password.data, "sha256"),
                   email=form.email.data, admin=form.admin.data)
        db.session.add(usr)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/new_user.html', title='Signup', form=form)


@admin.route("/admin/users/<user_id>/delete")
@requires_access_level()
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for("admin.users"))


@admin.route('/admin/users/<user_id>/schedules', methods=['GET', 'POST'])
@requires_access_level()
def user_schedules(user_id):
    all_schedules = Schedule.query.filter_by(id_user=user_id).all()
    user = User.query.filter_by(id=user_id).first()
    return render_template('schedule/all_schedules.html', schedules=all_schedules, user=user)


@admin.route('/admin/users/<user_id>/alarms', methods=['GET', 'POST'])
@requires_access_level()
def user_alarms(user_id):
    all_alarms = Alarm.query.filter_by(id_user=user_id).all()
    user = User.query.filter_by(id=user_id).first()
    return render_template('alarm/all_alarms.html', alarms=all_alarms, user=user)


@admin.route("/admin/schedules", methods=['GET'])
@requires_access_level()
def schedules():
    admin_schedules = Schedule.query.all()
    all_users = User.query.all()
    return render_template('admin/all_schedules.html', schedules=admin_schedules, users=all_users, admin=True)


@admin.route('/admin/schedules/<int:schedule_id>', methods=['GET', 'POST'])
@requires_access_level()
def schedule(schedule_id):
    sch = Schedule.query.filter_by(id=schedule_id).first()
    all_daily_schedules = DailySchedule.query.filter_by(object_id=schedule_id).all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    current_days = list()
    special_days = list()
    visto = False
    i = 0
    j = 0
    rex = re.compile("[0-2][0-9][0-9][0-9]-[0-3][0-9]-[0-3][0-9]")

    for week_day in days:
        for day in all_daily_schedules:
            if week_day == day.day and not visto:
                current_days.insert(i, week_day)
                visto = True
        i = i + 1
        visto = False

    for day in all_daily_schedules:
        if rex.match(day.day):
            special_days.insert(j, day)
            j = j + 1

    return render_template('schedule/schedule.html', days=current_days, schedule=sch,
                           daily_schedules=all_daily_schedules, special_days=special_days, user=True)


@admin.route('/admin/schedules/<int:schedule_id>/update', methods=['GET', 'POST'])
@requires_access_level()
def update_schedule(schedule_id):
    form = SchedulesRegisterForm()
    sch = Schedule.query.filter_by(id=schedule_id).first()
    if form.validate_on_submit():
        sch.object_name = form.object_name.data,
        sch.object_type = form.object_type.data,
        sch.present_value = form.present_value.data,
        sch.description = form.description.data,
        sch.effective_period = form.effective_period.data,
        sch.exception_schedule = form.exception_schedule.data,
        sch.list_of_object_property_references = form.list_of_object_property_references.data,
        sch.priority_for_writing = form.priority_for_writing.data,
        sch.status_flags = form.status_flags.data,
        sch.reliability = form.reliability.data,
        sch.out_of_service = form.out_of_service.data
        user = User.query.filter_by(usr=form.id_user.data).first()
        sch.id_user = user.id
        db.session.add(sch)
        db.session.commit()
        flash(f'Object updated id object {form.object_identifier.data}', 'success')
        return redirect(url_for('admin.schedule', user_id=user.id, schedule_id=sch.id))
    all_users = User.query.all()
    user = User.query.filter_by(id=sch.id_user).first()
    return render_template('schedule/register.html', title='Update Schedule', form=form, schedule=sch, user=user,
                           users=all_users)


@admin.route("/admin/schedules/register", methods=['GET', 'POST'])
@requires_access_level()
def register_schedule():
    form = SchedulesRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(usr=form.id_user.data).first()
        sch = Schedule(
            object_identifier=form.object_identifier.data,
            object_name=form.object_name.data,
            object_type=form.object_type.data,
            present_value=form.present_value.data,
            description=form.description.data,
            effective_period=form.effective_period.data,
            exception_schedule=form.exception_schedule.data,
            list_of_object_property_references=form.list_of_object_property_references.data,
            priority_for_writing=form.priority_for_writing.data,
            status_flags=form.status_flags.data,
            reliability=form.reliability.data,
            out_of_service=form.out_of_service.data,
            id_user=user.id
        )
        db.session.add(sch)
        db.session.commit()
        flash(f'Object registered id object {form.object_identifier.data}', 'success')
        return redirect(url_for('admin.users'))
    all_users = User.query.all()
    return render_template('schedule/register.html', title='Register Schedule', form=form, admin=True, users=all_users)


@admin.route('/admin/alarms', methods=['GET', 'POST'])
@requires_access_level()
def alarms():
    all_alarms = Alarm.query.all()
    all_users = User.query.all()
    return render_template('admin/all_alarms.html', alarms=all_alarms, users=all_users)


@admin.route('/admin/alarms/<int:alarm_id>/update', methods=['GET', 'POST'])
@requires_access_level()
def update_alarm(alarm_id):
    form = AlarmsRegisterForm()
    alarm = Alarm.query.filter_by(id=alarm_id).first()
    states = ['Active', 'Inactive']
    events = ['Normal', 'Offnormal', 'Fault']
    if form.validate_on_submit():
        alarm.state = form.state.data
        alarm.event = form.event.data
        alarm.source = form.source.data
        alarm.source_description = form.source_description.data
        alarm.triggered_time = form.triggered_time.data
        user = User.query.filter_by(usr=form.id_user.data).first()
        alarm.id_user = user.id
        db.session.add(alarm)
        db.session.commit()
        flash(f'Object updated id object {alarm.id}', 'success')
        return redirect(url_for('bacnet.alarms'))
    all_users = User.query.all()
    return render_template('alarm/register.html', title='Update Alarm', admin=True, form=form, alarm=alarm,
                           states=states, events=events, users=all_users)


@admin.route("/admin/alarms/register", methods=['GET', 'POST'])
@requires_access_level()
def register_alarm():
    form = AlarmsRegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(usr=form.id_user.data).first()
        alarm = Alarm(
            state=form.state.data,
            event=form.event.data,
            source=form.source.data,
            source_description=form.source_description.data,
            triggered_time=form.triggered_time.data,
            id_user=user.id
        )
        db.session.add(alarm)
        db.session.commit()
        flash(f'Object registered id object {form.state.data}', 'success')
        return redirect(url_for('bacnet.alarms'))
    all_users = User.query.all()
    return render_template('alarm/register.html', title='Register Schedule', form=form, admin=True, users=all_users)
