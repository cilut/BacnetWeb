CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    object_identifier VARCHAR,
    object_name VARCHAR,
    object_type VARCHAR,
    present_value VARCHAR,
    description VARCHAR,
    effective_period VARCHAR,
    exception_schedule VARCHAR,
    list_of_object_property_references VARCHAR,
    priority_for_writing VARCHAR,
    status_flags VARCHAR,
    reliability VARCHAR,
    out_of_service BOOLEAN,
    id_user INTEGER REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE dailySchedules(
    id SERIAL PRIMARY KEY,
    day VARCHAR,
    initial_time VARCHAR,
    final_time VARCHAR,
    value VARCHAR,
    object_id INTEGER REFERENCES schedules(id) ON DELETE CASCADE
);


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



class DailySchedule(UserMixin, db.Model):
    __tablename__ = "dailySchedules"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String, nullable=False)
    initial_time = db.Column(db.String, nullable=False)
    final_time = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)
    object_id = db.Column(db.Integer, nullable=False)