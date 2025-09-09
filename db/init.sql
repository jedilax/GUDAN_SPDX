-- runs automatically on first container start
CREATE TABLE IF NOT EXISTS USERS (
  uid INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  age INT NOT NULL
);
