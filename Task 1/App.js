var express = require('express');
var bodyParser = require('body-parser');
var path = require('path');

var app = express();

var quotes = [
	{
		'quote' : 'asfasfsdf'
	},
	{
		'quote' : 'bklmfgbfbgs'
	},
	{
		'quote' : 'gtrbgrthdfg'
	},
	{
		'quote' : 'fasdbfadasa'
	}
];

app.listen(3000,function(){
	console.log('Server started running of port 3000....');
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended : false}));

app.get('/rand',function(req,res){
	var ran = Math.floor(Math.random()*(quotes.length-1));
	res.json({
		'resquote' : quotes[ran],
		'error' : 'false'
	});
});

app.get('/getall',function(req,res){
	res.json({
		'allquotes': quotes,
		'error' : 'false'
	});
});
app.post('/addquote',function(req,res){
	if(!req.body.quote){
	    return res.json({
	    	message : 'Enter something',
	    	error : 'true'
	    });
	}

	quotes.push(req.body);
	return res.json({
		message : 'Success',
		error : 'false'
	});

});