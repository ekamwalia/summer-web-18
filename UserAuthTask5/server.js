const express = require('express');
const app = express();
const session = require('express-session');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const mysql = require('mysql');
const bcrypt = require('bcrypt');

var connection = mysql.createConnection({
	host : 'localhost',
	user: 'root',
	password: '',
	database: 'summer_web_project'
});
connection.connect();

app.use(bodyParser.json());
app.use(cookieParser());
app.use(session({secret:'secret'}));


app.post('/register',(req,res)=>{
	const uidQuery ="SELECT * FROM users WHERE userid=?";
	bcrypt.hash(req.body.password,10,(err,hash)=>{
		if(err)
			console.log(err);
		else
		{
			connection.query(uidQuery,[req.body.userid],(err,rows,fields)=>{
		if(rows.length)
			res.json({'status':'failed.userid already exists.'});
		else
			connection.query("INSERT INTO users VALUES (?,?)",[req.body.userid,hash],(error,results)=>{
				if(err)
					console.log(error);
				else
					res.json({'status':'success'});
			});
	});
		}
	});
});

app.post('/login',(req,res)=>{
	const passQuery ="SELECT password FROM users WHERE userid=? LIMIT 1";
	connection.query(passQuery,[req.body.userid],(err,rows,fields)=>{
		if(!rows.length)
			res.json({'status':'User not found'});
		else
			bcrypt.compare(req.body.password,rows[0].password,(error,result)=>{
				if(result)
				{
					req.session.userid = req.body.userid;
					res.json({"status":'logged in'});
				}
				else
					res.json({'status':'wrong password'});
			});
	});
});

app.get('/home',(req,res)=>
{
	if(!req.session.userid)
		res.json({'status':'Log in required'});
	else
	{
		let msg = "Welcome!"+req.session.userid+"!!";
		res.json({'message':msg});
	}
});

app.post('/logout',(req,res)=>{
	req.session.destroy((err)=>{
		if(err)
			console.log(err);
		else
			res.json({'status':'logged out successfully'});
	});
});

app.listen(3000,(err)=>
{
	if(err)
		console.log(err);
	else
		console.log('Listening on 3000!');
});
