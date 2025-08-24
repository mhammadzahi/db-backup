-- 1. ADMINS
CREATE TABLE admins (
    admin_id     SERIAL PRIMARY KEY,
    full_name    TEXT    NOT NULL,
    company_name TEXT    NOT NULL,
    email        TEXT    UNIQUE NOT NULL,
    password_    TEXT    NOT NULL,
    created_at   TIMESTAMP NOT NULL
);

-- 2. EMPLOYEES
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    admin_id    INTEGER   NOT NULL REFERENCES admins(admin_id),
    full_name   TEXT      NOT NULL,
    email       TEXT      UNIQUE NOT NULL,
    password_   TEXT      NOT NULL,
    department  TEXT,
    created_at  TIMESTAMP NOT NULL
);

-- 3. LOCATIONS
CREATE TABLE locations (
    location_id SERIAL PRIMARY KEY,
    employee_id INTEGER   NOT NULL REFERENCES employees(employee_id),
    latitude    NUMERIC   NOT NULL,
    longitude   NUMERIC   NOT NULL,
    timestamp   TIMESTAMP NOT NULL
);


-- 4. DAILY_REPORTS
CREATE TABLE daily_reports (
    employee_id  INTEGER   NOT NULL REFERENCES employees(employee_id),
    date         DATE      NOT NULL,
    "in"         TIME,
    "out"        TIME,
    start_break  TIME,
    end_break    TIME,
    PRIMARY KEY (employee_id, date)
);

-- 5. Logs
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    action TEXT,
    action_type VARCHAR(20),
    datetime TIMESTAMP WITHOUT TIME ZONE
);

-- 6. UNIQUE CONSTRAINTS
ALTER TABLE locations
ADD CONSTRAINT unique_employee_location_time
UNIQUE (employee_id, latitude, longitude, timestamp);
