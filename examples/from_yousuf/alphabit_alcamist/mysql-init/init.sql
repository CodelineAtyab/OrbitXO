CREATE DATABASE IF NOT EXISTS api_log_db;
USE api_log_db;

CREATE TABLE IF NOT EXISTS requests_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp VARCHAR(50) NOT NULL,
  input_string TEXT,
  output_data JSON
);
