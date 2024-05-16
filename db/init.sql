CREATE DATABASE IF NOT EXISTS meet_team;

use meet_team
;

CREATE TABLE IF NOT EXISTS `user` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	account VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	name VARCHAR(255) NOT NULL,
	description VARCHAR(500),
	join_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(account)
);

CREATE TABLE IF NOT EXISTS `course` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	owner_id INT,
	year INT NOT NULL,
	semester ENUM('1', '2') NOT NULL,
	description VARCHAR(50),
	launch_at TIMESTAMP DEFAULT NOW(),
	FOREIGN KEY(owner_id) REFERENCES `user`(id)
);

CREATE TABLE IF NOT EXISTS `course_member` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
	course_id INT,
	role ENUM('Prof', 'TA', 'Stu') DEFAULT 'Stu',
	join_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(user_id, course_id),
	FOREIGN KEY(user_id) REFERENCES `user`(id),
	FOREIGN KEY(course_id) REFERENCES `course`(id)
);

CREATE TABLE IF NOT EXISTS `group` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	course_id INT,
	owner_id INT,
	name VARCHAR(50) NOT NULL,
	description VARCHAR(500),
	create_at TIMESTAMP DEFAULT NOW(),
	UNIQUE(course_id, name),
	FOREIGN KEY(owner_id) REFERENCES `user`(id),
	FOREIGN KEY(course_id) REFERENCES `course`(id)
);

CREATE TABLE IF NOT EXISTS `group_member` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	user_id INT,
	group_id INT,
	join_at TIMESTAMP DEFAULT NOW(),
	FOREIGN KEY(user_id) REFERENCES `user`(id),
	FOREIGN KEY(group_id) REFERENCES `group`(id)
);

CREATE TABLE IF NOT EXISTS `task` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	name TEXT,
	group_id INT,
	creator_id INT,
	assignee_id INT,
	reviewer_id INT,
	description TEXT,
	create_at TIMESTAMP DEFAULT NOW(),
	close_at TIMESTAMP DEFAULT NULL,
	status ENUM('Todo', 'Doing', 'Done') DEFAULT 'Todo',
	FOREIGN KEY(group_id) REFERENCES `group`(id),
	FOREIGN KEY(creator_id) REFERENCES `user`(id),
	FOREIGN KEY(assignee_id) REFERENCES `user`(id),
	FOREIGN KEY(reviewer_id) REFERENCES `user`(id)
);

CREATE TABLE IF NOT EXISTS `commit` (
	id INT AUTO_INCREMENT PRIMARY KEY,
	task_id INT,
	creator_id INT,
	title VARCHAR(50),
	description TEXT,
	reference_link TEXT,
	create_at TIMESTAMP DEFAULT NOW(),
	FOREIGN KEY(creator_id) REFERENCES `user`(id),
	FOREIGN KEY(task_id) REFERENCES `task`(id)
);
