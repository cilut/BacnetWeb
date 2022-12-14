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


