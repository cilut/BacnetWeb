import re

from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user

from bacnetweb import db
from bacnetweb.access_level import requires_access_schedule, requires_access_alarm
from bacnetweb.forms.routes import SchedulesRegisterForm, DailyScheduleRegisterForm, \
    SpecialScheduleRegisterForm, AlarmsRegisterForm
from bacnetweb.models import Schedule, DailySchedule, Alarm

bacnet = Blueprint('bacnet', __name__)


@bacnet.route("/schedules", methods=['GET'])
@login_required
def schedules():
    all_schedules = Schedule.query.filter_by(id_user=current_user.id).all()
    return render_template('schedule/all_schedules.html', schedules=all_schedules)


@bacnet.route("/schedule", methods=['GET', 'POST'])
@login_required
def registerSchedule():
    form = SchedulesRegisterForm()
    if form.validate_on_submit():
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
            id_user=current_user.id
        )
        db.session.add(sch)
        db.session.commit()
        flash(f'Object registered id object {form.object_identifier.data}', 'success')
        return redirect(url_for('bacnet.schedules'))
    return render_template('schedule/register.html', title='Register Schedule', form=form)


@bacnet.route("/schedule/<int:schedule_id>/update", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def updateSchedule(schedule_id):
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

        db.session.add(sch)
        db.session.commit()
        flash(f'Object updated id object {form.object_identifier.data}', 'success')
        return redirect(url_for('bacnet.schedules'))
    return render_template('schedule/register.html', title='Update Schedule', form=form, schedule=sch)


@bacnet.route("/schedule/<int:schedule_id>", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def schedule(schedule_id):
    sch = Schedule.query.get_or_404(schedule_id)
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
                           daily_schedules=all_daily_schedules, special_days=special_days)


@bacnet.route("/schedule/<int:schedule_id>/delete", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def delete_schedule(schedule_id):
    Schedule.query.filter_by(id=schedule_id, id_user=current_user.id).delete()
    db.session.commit()
    return redirect(url_for('bacnet.schedules'))


@bacnet.route("/schedule/<int:schedule_id>/daily_sch", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def add_daily(schedule_id):
    form = DailyScheduleRegisterForm()
    if form.validate_on_submit():
        day_sch = DailySchedule(
            day=form.day.data,
            initial_time=form.initial_time.data,
            final_time=form.final_time.data,
            value=form.value.data,
            object_id=schedule_id
        )
        db.session.add(day_sch)
        db.session.commit()
        flash(f'Daily schedule registered', 'success')
        return redirect(url_for('bacnet.schedule', schedule_id=schedule_id))
    return render_template('schedule/new_daily_schedule.html', form=form, schedule_id=schedule_id, title="Daily")


@bacnet.route("/schedule/<int:schedule_id>/special_sch", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def add_special(schedule_id):
    form = SpecialScheduleRegisterForm()
    if form.validate_on_submit():
        day_sch = DailySchedule(
            day=form.day.data,
            initial_time=form.initial_time.data,
            final_time=form.final_time.data,
            value=form.value.data,
            object_id=schedule_id
        )
        db.session.add(day_sch)
        db.session.commit()
        flash(f'Daily schedule registered', 'success')
        return redirect(url_for('bacnet.schedule', schedule_id=schedule_id))
    return render_template('schedule/new_daily_schedule.html', form=form, schedule_id=schedule_id, title="Special")


@bacnet.route("/schedule/<int:schedule_id>/daily_sch/<daily_id>", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def update_daily(schedule_id, daily_id):
    form = DailyScheduleRegisterForm()
    current_daily_sch = DailySchedule.query.filter_by(id=daily_id).first()
    if form.validate_on_submit():
        current_daily_sch.day = form.day.data
        current_daily_sch.initial_time = form.initial_time.data
        current_daily_sch.final_time = form.final_time.data
        current_daily_sch.value = form.value.data
        current_daily_sch.object_id = schedule_id

        db.session.add(current_daily_sch)
        db.session.commit()
        flash(f'Daily schedule updated', 'success')
        return redirect(url_for('bacnet.schedule', schedule_id=schedule_id))
    return render_template('schedule/update_daily_schedule.html', form=form, current_daily_sch=current_daily_sch)


@bacnet.route("/schedule/<int:schedule_id>/special_sch/<special_id>", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def update_special(schedule_id, special_id):
    form = SpecialScheduleRegisterForm()
    current_daily_sch = DailySchedule.query.filter_by(id=special_id).first()

    if form.validate_on_submit():
        current_daily_sch.day = form.day.data
        current_daily_sch.initial_time = form.initial_time.data
        current_daily_sch.final_time = form.final_time.data
        current_daily_sch.value = form.value.data
        current_daily_sch.object_id = schedule_id

        db.session.add(current_daily_sch)
        db.session.commit()
        flash(f'Special schedule updated', 'success')
        return redirect(url_for('bacnet.schedule', schedule_id=schedule_id))

    return render_template('schedule/update_daily_schedule.html', form=form, current_daily_sch=current_daily_sch,
                           title="Special")


@bacnet.route("/schedule/<int:schedule_id>/daily_sch/<daily_id>/delete", methods=['GET', 'POST'])
@login_required
@requires_access_schedule
def delete_daily(schedule_id, daily_id):
    DailySchedule.query.filter_by(id=daily_id).delete()
    db.session.commit()
    return redirect(url_for('bacnet.schedule', schedule_id=schedule_id))


@bacnet.route("/alarms", methods=['GET'])
@login_required
def alarms():
    all_alarms = Alarm.query.filter_by(id_user=current_user.id).all()
    return render_template('alarm/all_alarms.html', alarms=all_alarms)


@bacnet.route("/alarm", methods=['GET', 'POST'])
@login_required
def registerAlarm():
    form = AlarmsRegisterForm()
    if form.validate_on_submit():
        alarm = Alarm(
            state=form.state.data,
            event=form.event.data,
            source=form.source.data,
            source_description=form.source_description.data,
            triggered_time=form.triggered_time.data,
            id_user=current_user.id
        )
        db.session.add(alarm)
        db.session.commit()
        flash(f'Object registered id object {form.state.data}', 'success')
        return redirect(url_for('bacnet.alarms'))
    return render_template('alarm/register.html', title='Register Schedule', form=form)


@bacnet.route("/alarm/<int:alarm_id>/update", methods=['GET', 'POST'])
@login_required
@requires_access_alarm
def updateAlarm(alarm_id):
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

        db.session.add(alarm)
        db.session.commit()
        flash(f'Object updated id object {alarm.id}', 'success')
        return redirect(url_for('bacnet.alarms'))
    return render_template('alarm/register.html', title='Update Alarm', form=form, alarm=alarm, states=states,
                           events=events)


@bacnet.route("/alarm/<int:alarm_id>/delete", methods=['GET', 'POST'])
@login_required
@requires_access_alarm
def delete_alarm(alarm_id):
    Alarm.query.filter_by(id=alarm_id).delete()
    db.session.commit()
    return redirect(url_for('bacnet.alarms'))
