const express = require('express');
const session = require('express-session');
const mysql = require('mysql2');
const bcrypt = require('bcrypt');
const bodyParser = require('body-parser');

const app = express();

// Middlewares

function auth(req, res, next) {
	const protected = ['/profile', '/logout'];
	if (protected.includes(req.url) && (!req.session || !req.session.authenticated)) {
		res.sendStatus(401);
		return;
	}
	next();
}

app.use(bodyParser.json());
app.use(session({
	secret: 'Cheeki Breeki Iv Damke',
	resave: false,
	saveUninitialized: true,
	cookie: {secure: false}
}));
app.use(auth);

function getConnection() {
	return mysql.createConnection({
		host: 'localhost',
		user: 'root',
		password: '',
		database: 'login'
	});
}

app.post('/register', (req, res) => {
	const conn = getConnection();
	const username = req.body.username;
	const password = req.body.password;

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
			res.send("Registered user successfully.");
		});
		conn.end();
	});
});

app.post('/login', (req, res) => {
	const conn = getConnection();
	const username = req.body.username;
	const password = req.body.password;

	const getHashQuery = "SELECT password_hash FROM users WHERE user_name = ? LIMIT 1";
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
					req.session.username = username;
					res.send("Login succeeded");
					conn.end();
				}
			});
		}
	});
});

app.get('/profile', (req, res) => {
	res.send("Welcome, " + req.session.username);
});

app.get('/logout', (req, res) => {
	res.clearCookie('connect.sid', {path: '/'});
	req.session.destroy((err) => {
		if(err) {
			console.log("Failed to destroy session: " + err);
			res.sendStatus(200);
			return;
		}
		res.send('You have been logged out');
	});
});

app.listen(4200, () => {
	console.log("Server is listening on port 4200");
});