CREATE TABLE IF NOT EXISTS requests_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    input_string TEXT,
    output_data TEXT
);