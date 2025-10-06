CREATE TABLE IF NOT EXISTS request_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    input_data TEXT NOT NULL,
    output_data JSON NOT NULL
);
