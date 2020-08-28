CREATE TABLE alarms (
    id SERIAL PRIMARY KEY,
    state VARCHAR,
    event VARCHAR,
    source VARCHAR,
    source_description VARCHAR,
    alarm_text VARCHAR,
    triggered_time VARCHAR,
    id_user INTEGER REFERENCES users(id) ON DELETE CASCADE
);