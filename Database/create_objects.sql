CREATE TABLE Objects (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR
);


CREATE TABLE  DeviceObjects(
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR,
    vendor_name VARCHAR
);
