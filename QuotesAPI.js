var express = require('express');
var app = express();
var bodyParser = require('body-parser');

app.listen(3000, (err)=>{
	if(err)
		console.log(err);
	else
		console.log('Listening to port 3000');
});
app.use(bodyParser.json());

var cont = ['Lol noob','GG','ez'];

app.get('/rand',(req,res)=>{
	var a = Math.floor(Math.random() * cont.length)
	res.json({'quote' : cont[a]});
	res.end();
});

app.delete('/delete/:id',(req,res)=>{
	var delId = req.params.id -1 ;
	cont.splice(delId,1);
	res.json({"message":"quote deleted"});
});

app.post('/add',(req,res)=>{
	var val = req.body;
	cont.push(val.quote);
	res.json({"message":"quote added"});
});
