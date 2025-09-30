CREATE DATABASE IF NOT EXISTS measurements;
USE measurements;

-- ensure root is available via mysql_native_password (compatible with many clients)
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root';
FLUSH PRIVILEGES;

CREATE TABLE IF NOT EXISTS history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_str VARCHAR(2549) NOT NULL,
    result_str VARCHAR(2549) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
