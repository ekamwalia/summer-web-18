var express = require('express');
var bodyParser = require('body-parser');
var app = express();

app.use(bodyParser.json());

var quotes = [
	'Did you ever hear the tragedy of Darth Plagueis The Wise?',
	'I thought not.',
	'It’s not a story the Jedi would tell you.',
	'It’s a Sith legend.',
	'Darth Plagueis was a Dark Lord of the Sith, so powerful and so wise he could use the Force to influence the midichlorians to create life.',
	'He had such a knowledge of the dark side that he could even keep the ones he cared about from dying.',
	'The dark side of the Force is a pathway to many abilities some consider to be unnatural.',
	'He became so powerful the only thing he was afraid of was losing his power, which eventually, of course, he did.',
	'Unfortunately, he taught his apprentice everything he knew, then his apprentice killed him in his sleep.',
	'Ironic.',
	'He could save others from death, but not himself.',
]

app.get('/all', (req, res) => {
	res.setHeader('Content-Type', 'application/json');
	res.send(JSON.stringify(quotes));
	res.end();
});

app.get('/:id', (req, res) => {
	var id = req.params.id;
	if (id < quotes.length) {
		res.setHeader('Content-Type', 'application/json');
		res.send(JSON.stringify({ "quote": quotes[id] }));
	} else {
		res.statusCode = 404;
	}
	res.end();
});

app.get('/rand', (req, res) => {
	var r = Math.floor(Math.random() * quotes.length);
	res.setHeader('Content-Type', 'application/json');
	res.send(JSON.stringify({"quote": quotes[r]}));
	res.end();
});

app.post('/add', (req, res) => {
	var quote = req.body;
	quotes.push(quote);
	res.setHeader('Content-Type', 'application/json');
	res.send('Quote added successfully' + quote);
	res.end();
});

app.delete('/del/:id', (req, res) => {

});

app.listen(4200, () => console.log('Listening on port 4200'));
