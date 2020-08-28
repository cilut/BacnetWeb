CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    usr VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    email VARCHAR NOT NULL
);

ALTER TABLE users
ADD COLUMN email_confirmed_at VARCHAR;