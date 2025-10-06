-- This script will be executed when the database container is first created.
-- It ensures the necessary table exists before the application tries to use it.

USE log_db;

CREATE TABLE IF NOT EXISTS requests_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(255) NOT NULL,
    input_string TEXT NOT NULL,
    output_data TEXT NOT NULL
);