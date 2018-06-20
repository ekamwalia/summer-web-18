const mysql = require('mysql2');

const config = {
	host: 'localhost',
	user: 'root',
	password: '',
	database: 'github_frontend'
};

module.exports = () => mysql.createConnection(config);