CREATE TABLE IF NOT EXISTS student_performance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    subject VARCHAR(50) NOT NULL,
    marks NUMERIC(5,2) NOT NULL,
    pass_fail VARCHAR(4) NOT NULL,
    grade VARCHAR(1) NOT NULL,
    processed_at TIMESTAMP NOT NULL
);