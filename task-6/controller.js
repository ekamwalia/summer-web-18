const request = require('request');
const mysql = require('mysql2');
const bcrypt = require('bcrypt');

const createConn = require('./createConn');

const apiCall = (endpoint, callback) => {
	request({
		url: 'https://api.github.com' + endpoint,
		headers: {
			'User-Agent': 'Github Frontend',
			'Accept': 'application/vnd.github.v3.raw+json'
		}
	}, callback);
};

exports.GET_register = (req, res) => {
	res.render('register');
};

exports.POST_register = (req, res) => {
	const username = req.body.username;
	const password = req.body.password;

	if (!username) {
		res.send("Username must not be empty");
		return;
	} else if (!password) {
		res.send("Password must not be empty");
		return;
	}

	const conn = createConn();
	const check = "SELECT * FROM users WHERE user_name = ? LIMIT 1";
	conn.query(check, [username], (err, rows, fields) => {
		if (err) {
			console.log("Failed to query database: " + err);
			res.sendStatus(200);
			conn.end();
			return;
		} else if (rows.length) {
			res.send("User already exists");
			conn.end();
			return;
		} else {
			const query = "INSERT INTO users(user_name, password_hash) VALUES(?, ?)";
			bcrypt.hash(password, 10, (err, hash) => {
				if (err) {
					console.log("Failed to hash password: " + err);
					res.sendStatus(500);
					conn.end();
					return;
				}
				conn.query(query, [username, hash], (err, rows, fields) => {
					if (err) {
						console.log("Failed to add user: " + err);
						res.sendStatus(500);
						conn.end();
						return;
					}
					res.send("Registered user successfully");
					conn.end();
				});
			});
		}
	});
}

exports.GET_login = (req, res) => {
	res.render('login');
};

exports.POST_login = (req, res) => {
	const username = req.body.username;
	const password = req.body.password;

	if (!username) {
		res.send("Username must not be empty");
		return;
	} else if (!password) {
		res.send("Password must not be empty");
		return;
	}

	const conn = createConn();

	const getHashQuery = "SELECT * FROM users WHERE user_name = ? LIMIT 1";
	conn.query(getHashQuery, [username], (err, rows, fields) => {
		if (err) {
			console.log("Failed to query hash: " + err);
			conn.end();
			return;
		} else if (rows.length == 0) {
			res.send("Login failed: Invalid username");
			conn.end();
			return;
		} else {
			const userId = rows[0].id;
			bcrypt.compare(password, rows[0].password_hash, (err, same) => {
				if (err) {
					console.log("Failed to compare hashes: " + err);
					conn.end();
					return;
				} else if (!same) {
					res.send("Login failed: Invalid password");
					conn.end();
					return;
				} else {
					req.session.authenticated = true;
					req.session.userId = userId;
					req.session.username = username;
					res.redirect('/profile');
					conn.end();
				}
			});
		}
	});
};

exports.GET_profile = (req, res) => {
	const conn = createConn();
	const getStarred = "SELECT starred_user_name FROM starred_users WHERE id = ?";
	let starredUsers = [];
	conn.query(getStarred, [req.session.userId], (err, rows, fields) => {
		if (err) {
			console.log("Failed to query starred users: ");
			return;
		} else if(rows.length == 0) {
			starredUsers = null;
		} else {
			starredUsers = rows.map(r => r.starred_user_name);
		}

		res.render('profile', {
			username: req.session.username,
			starredUsers: starredUsers
		});
	});
	conn.end();
};

exports.POST_search = (req, res) => {
	req.session.searchedUser = req.body.search;
	res.redirect('/user/' + req.session.searchedUser);
};

exports.GET_user = (req, res) => {
	const searchedUser = req.params.owner;
	req.session.searchedUser = searchedUser;
	apiCall('/users/' + searchedUser + '/repos', (err, result, body) => {
		const reposJSON = JSON.parse(body);
		const searchedUserRepos = Object.keys(reposJSON).map(key => reposJSON[key].name);
		res.render('user', {
			username: req.session.username,
			user: searchedUser,
			userRepos: searchedUserRepos
		});
	});
};

exports.POST_star = (req, res) => {
	res.redirect('/user/' + req.session.searchedUser);
};

exports.GET_repo = (req, res) => {
	const searchedUser = req.params.owner;
	const selectedRepo = req.params.repo;
	const endPoint = '/repos/' + searchedUser + '/' + selectedRepo + '/contents';
	apiCall(endPoint, (err, result, body) => {
		const contentsJSON = JSON.parse(body);
		const contents = Object.keys(contentsJSON).map(key => contentsJSON[key].name);
		res.render('repo', {
			repo: selectedRepo,
			path: '',
			items: contents
		});
	});
};

exports.GET_repoContents = (req, res) => {
	const searchedUser = req.params.owner;
	const selectedRepo = req.params.repo;
	const pathInRepo = req.params['0'];
	const endPoint = '/repos/' + searchedUser + '/' + selectedRepo + '/contents' + pathInRepo;
	request({
		url: 'https://api.github.com' + endPoint,
		headers: {
			'User-Agent': 'Github Frontend'
		}
	}, (err, result, body) => {
		// TODO: Can't differentiate between file and folder
		const contentsJSON = JSON.parse(body);
		if (!contentsJSON.type) {
			// Is a directory
			const contents = Object.keys(contentsJSON).map(key => contentsJSON[key].name);
			res.render('repo', {
				repo: selectedRepo,
				path: pathInRepo,
				items: contents
			});
		} else 	{
			// Is a file
			apiCall(endPoint, (err, result, body) => {
				res.render('file', {
					repo: selectedRepo,
					path: pathInRepo,
					source: body
				});
			});
		}
	});
}

exports.POST_logout = (req, res) => {
	res.clearCookie('connect.sid', { path: '/' });
	req.session.destroy((err) => {
		if (err) {
			console.log("Failed to destroy session: " + err);
			res.sendStatus(200);
			return;
		}
		res.render('logout');
	});
};

exports.GET_boilerplate = (req, res) => {
	res.render('includes/layout.pug');
};