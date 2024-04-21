CREATE DATABASE IF NOT EXISTS meet_team;

CREATE TABLE IF NOT EXISTS user (
	id serial PRIMARY KEY,
	account VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR(500),
	join_at timestamp DEFAULT now(),
	UNIQUE(account)
);

CREATE TABLE IF NOT EXISTS course (
	id serial PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	owner_id int REFERENCES user(id),
	description varchar(50) NOT NULL,
	launch_at timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS course_member (
	id serial PRIMARY KEY,
	user_id int REFERENCES user(id),
	event_id int REFERENCES event(id),
	role ENUM('Prof', 'TA', 'Stu') DEFAULT 'Stu',
	join_at timestamp DEFAULT now(),
	UNIQUE(user_id, event_id)
);

-- below statements has not been already tested
CREATE TABLE IF NOT EXISTS annoucement (
	id serial PRIMARY KEY,
	status PUBLISH_STATUS DEFAULT 'draft',
	member_id serial REFERENCES member(id),
	topic varchar(50),
	content VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS task (
	id serial PRIMARY KEY,
	event_id serial REFERENCES event(id),
	creator_id serial REFERENCES user(id),
	name varchar(30) NOT NULL,
	description VARCHAR(255),
	create_at timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS reviewer (
	id serial PRIMARY KEY,
	task_id serial REFERENCES task(id),
	user_id seiral REFERENCES user(id),
    assigned_at timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS commit (
	id serial PRIMARY KEY,
	task_id serial REFERENCES task(id),
	user_id serial REFERENCES user(id),
	message VARCHAR(50) NOT NULL,
	create_at timestamp DEFAULT now()
);

CREATE TABLE IF NOT EXISTS message (
	id serial PRIMARY KEY,
	task_id serial REFERENCES event(id),
	sender_id serial REFERENCES user(id),
	content VARCHAR(255) NOT NULL,
	create_at timestamp DEFAULT now()
);
