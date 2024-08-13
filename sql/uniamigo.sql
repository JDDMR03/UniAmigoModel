CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(999) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
);

CREATE TABLE unhandled_messages (
    message_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
