DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS tools CASCADE;
DROP TABLE IF EXISTS logs CASCADE;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    username varchar(20) UNIQUE NOT NULL,
    password varchar(60) NOT NULL,
    role varchar(10) NOT NULL,
    manager uuid,
	CONSTRAINT fk_manager FOREIGN KEY(manager) REFERENCES users(id)
);
CREATE TABLE tools (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name varchar(50) NOT NULL,
    description varchar(200) NOT NULL,
    brand varchar(50) NOT NULL,
	image varchar(50) NOT NULL,
    manager uuid NOT NULL,
    worker uuid,
	approved boolean NOT NULL,
	CONSTRAINT fk_manager FOREIGN KEY(manager) REFERENCES users(id),
	CONSTRAINT fk_worker FOREIGN KEY(worker) REFERENCES users(id)
);
CREATE TABLE logs (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    worker_username varchar(20) NOT NULL,
    tool_name varchar(50) NOT NULL,
    manager uuid NOT NULL,
    borrowed_at timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    returned_at timestamp,
	CONSTRAINT fk_manager FOREIGN KEY(manager) REFERENCES users(id)
);

SELECT * FROM users;
SELECT * FROM tools;
SELECT * FROM logs;
