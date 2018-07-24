const express = require('express');
const app = express();
const session = require('express-session');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const bcrypt = require('bcrypt');
const request = require('request');
const path = require('path');

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended : true}));
app.use(session({secret:"secret"}));

var connection = mysql.createConnection({
	host : 'localhost',
	user: 'root',
	password: '',
	database: 'summer_web_project'
});

function checkAuth(req, res, next)
{
	if(req.session.userid)
		return next();
	else
		res.send('Log in required');
}

app.get('/login',(req,res)=>{
    res.sendFile(path.join(__dirname,'/front'),'login.html');
});

app.get('/register',(req,res)=>{
	res.sendFile(path.join(__dirname,'/front'),'register.html');
})

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
					res.redirect('/search');
				}
				else
					res.json({'status':'wrong password'});
			});
	});
});

app.get('/search', checkAuth, (req,res)=>{
	res.render(path.join(__dirname,'/front'),search.html);
});

app.post('/search', checkAuth, (req,res)=>{
	var redURL = '/user/' + req.body.username;
	res.redirect(redURL);
});

app.get('/user/:user',  (req,res)=>{
	const user = req.params.user;
	const userReq = 'http://api.github.com/users/' + user + '/repos';
	request({url:userReq, headers:{'User-Agent':'Github Frontend', 'Accept' : 'application/vnd.github.v3raw+json'}},(err,result,body)=>{
		var repos = JSON.parse(body);
		var txt = 'Repositories: \n \n';
		var t=1;
		for(x in repos)
		{
			txt += t + '. ' + repos[x].name + '\n';
			t++;
		}
		res.send(txt);
	});
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
