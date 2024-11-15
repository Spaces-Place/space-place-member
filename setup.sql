CREATE DATABASE IF NOT EXISTS spaceplaceDB;
USE spaceplaceDB;

-- MEMBER 테이블 생성
CREATE TABLE IF NOT EXISTS Member (
    id INT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    type ENUM('vendor', 'consumer'),
    create_date DATETIME
);

CREATE INDEX IF NOT EXISTS idx_user_id ON space (user_id);