CREATE TABLE IF NOT EXISTS travel_time_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    source VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    duration_minutes INT NOT NULL,
    distance VARCHAR(100),
    distance_value INT,
    is_minimum BOOLEAN DEFAULT FALSE
);