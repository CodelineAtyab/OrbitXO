-- Initialize the database and history table

USE api_log_db;

CREATE TABLE IF NOT EXISTS requests_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(255) NOT NULL,
    input_string TEXT NOT NULL,
    output_data TEXT NOT NULL
);
