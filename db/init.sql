CREATE DATABASE IF NOT EXISTS meet_team;

CREATE TABLE IF NOT EXISTS user (
	id serial PRIMARY KEY,
	account VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR(500),
	join_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(account)
);

CREATE TABLE IF NOT EXISTS course (
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	owner_id INT REFERENCES user(id),
	year INT NOT NULL,
	semester ENUM('1', '2') NOT NULL,
	description VARCHAR(50),
	launch_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS course_member (
	id SERIAL PRIMARY KEY,
	user_id INT REFERENCES user(id),
	course_id INT REFERENCES event(id),
	role ENUM('Prof', 'TA', 'Stu') DEFAULT 'Stu',
	join_at TIMESTAMP DEFAULT now(),
	UNIQUE(user_id, course_id)
);

CREATE TABLE IF NOT EXISTS `group` (
	id SERIAL PRIMARY KEY,
	course_id INT REFERENCES course(id),
	owner_id INT REFERENCES user(id),
	name VARCHAR(50) NOT NULL,
	description VARCHAR(500),
	create_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(course_id, name)
);

CREATE TABLE IF NOT EXISTS group_member (
	id SERIAL PRIMARY KEY,
	user_id INT REFERENCES user(id),
	group_id INT REFERENCES `group`(id),
	join_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS task (
	id SERIAL PRIMARY KEY,
	name TEXT,
	group_id INT REFERENCES `group`(id),
	creator_id INT REFERENCES user(id),
	assignee_id INT REFERENCES user(id),
	reviewer_id INT REFERENCES user(id),
	description TEXT,
	create_at TIMESTAMP DEFAULT NOW(),
	close_at TIMESTAMP DEFAULT NULL,
	status ENUM('Todo', 'Doing', 'Done') DEFAULT 'Todo'

);

CREATE TABLE IF NOT EXISTS commit (
	id SERIAL PRIMARY KEY,
	task_id INT REFERENCES task(id),
	creator_id INT REFERENCES user(id),
	description TEXT,
	reference_link TEXT
);
