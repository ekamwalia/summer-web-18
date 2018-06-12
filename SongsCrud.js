var express = require("express");
var app = express();
var mysql = require("mysql");

var connection = mysql.createConnection({
	host : 'localhost',
	user: 'root',
	password: '',
	database: 'summer_web_project'
});
connection.connect();

var bodyParser = require("body-parser");
app.use(bodyParser.json());

app.listen(3000,(err)=>
{
	if(err)
		console.log(err);
	else
		console.log('Listening on 3000!');
});

app.post('/song',(req,res)=>{
	var val = req.body;

	connection.query("INSERT INTO songs ( title, rating) VALUES (?,?);",[val.title,val.rating],(err,result)=>{
		if(err)
			console.log(err);
		else
			res.json({"status":"success"});
	});
});

app.delete('/song',(req,res)=>{
	var val = req.body;

	connection.query("DELETE FROM songs WHERE title=?",[val.title],(err,result)=>{
		if(err)
			console.log(err);
		else
			res.json({"status":"success","Rows deleted":result.affectedRows});
	});
});

app.put('/song',(req,res)=>{
	var val = req.body;

	connection.query("UPDATE songs SET rating=? WHERE title=?",[val.rating,val.title],(err,result)=>{
		if(err)
			console.log(err);
		else
			res.json({"status":"success","Rows changed":result.affectedRows});
	});
});

app.get('/song',(req,res)=>{
	connection.query("SELECT * FROM songs",(err, rows, fields)=>{
		if(err)
			console.log(err);
		else
		{
			res.json(rows);
		}
		
	});
});
