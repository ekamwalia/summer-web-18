const express = require('express');
const app = express();
const mysql = require('mysql');

const bodyParser = require('body-parser');

app.use(bodyParser.json());

function getConnection() {
	return mysql.createConnection({
		host: 'localhost',
		user: 'root',
		password: 'password',
		database: 'crud'
	});
}

// Add books
app.post('/create', (req, res) => {
	const conn = getConnection();
	const title = req.body.title;
	const author = req.body.author;

	const query = "INSERT INTO books(title, author) VALUES(?, ?)";
	conn.query(query, [title, author], (err, rows, fields) => {
		if (err) {
			console.log("Failed to add book: " + err);
			res.sendStatus(500);
			conn.end();
			return;
		}
		res.send("Created book successfully.");
		res.end();
	});
	conn.end();
});

// Query books by ID
app.get("/read/:id", (req, res) => {
	const conn = getConnection();

	const bookId = req.params.id;
	const query = "SELECT * FROM books WHERE id = ?";
	conn.query(query, [bookId], (err, rows, fields) => {
		if (err) {
			console.log("Failed to get book: " + err);
			res.sendStatus(404);
			conn.end();
			return;
		}

		res.json(rows);
	});
	conn.end();
});

app.post('/update/:id', (req,res) => {
	const conn = getConnection();

	const bookId = req.params.id;
	const title = req.body.title;
	const author = req.body.author;

	const query = "UPDATE books SET title = ?, author = ? WHERE id = ?";
	conn.query(query, [title, author, bookId], (err, rows, fields) => {
		if (err) {
			console.log("Failed to update book: " + err);
			res.sendStatus(500);
			conn.end();
			return;
		}
		res.send("Updated book successfully.");
		res.end();
	});
	conn.end();
});

app.delete('/delete/:id', (req, res) => {
	const conn = getConnection();

	const bookId = req.params.id;
	const query = "DELETE FROM books WHERE id = ?";
	conn.query(query, [bookId], (err, rows, fields) => {
		if (err) {
			console.log("Failed to delete book: " + err);
			res.sendStatus(500);
			conn.end();
			return;
		}
		res.send("Deleted book successfully");
		res.end();
	});
	conn.end();
});

app.listen(3003, () => {
	console.log("Server is listening on port 3003");
});