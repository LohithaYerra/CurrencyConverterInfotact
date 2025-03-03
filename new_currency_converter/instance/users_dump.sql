-- Start the transaction
START TRANSACTION;

-- Create the user table
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT, 
    username VARCHAR(150) NOT NULL, 
    email VARCHAR(150) NOT NULL, 
    password VARCHAR(200) NOT NULL, 
    PRIMARY KEY (id), 
    UNIQUE KEY (username), 
    UNIQUE KEY (email)
);

-- Insert data into the user table
INSERT INTO user (id, username, email, password) 
VALUES 
(1, 'Lohitha', 'lohitha48@gmail.com', 'pbkdf2:sha256:1000000$9VX3dY62xTxCElWx$2d490199e3aee4604b42b0ef6346363b2854a3bfb29d104554a9cd5337fb736e');

-- Commit the transaction
COMMIT;
