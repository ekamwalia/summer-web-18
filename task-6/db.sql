CREATE DATABASE github_frontend;
USE DATABASE github_frontend;

CREATE TABLE users (
	id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(32) NOT NULL,
	password_hash CHAR(61) NOT NULL
);

CREATE TABLE starred_users (
	id INT UNSIGNED NOT NULL,
	starred_user_name VARCHAR(32) NOT NULL,
	PRIMARY KEY(id, starred_user_name)
);