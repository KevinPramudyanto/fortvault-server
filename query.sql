DROP TABLE IF EXISTS users CASCADE;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    username varchar(20) UNIQUE NOT NULL,
    password varchar(60) NOT NULL,
    role varchar(10) NOT NULL,
    manager uuid,
	CONSTRAINT fk_manager FOREIGN KEY(manager) REFERENCES users(id)
);

SELECT * FROM users;