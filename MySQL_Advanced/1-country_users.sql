-- Create a table named `users` with the following columns:
DROP TABLE users;
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country Enum('US', 'CO', 'TN') NOT NULL DEFAULT 'US'
);
