var appRouter = function(app) {
	var quotes = ["Neo, sooner or later you're going to realize just as I did that there's a difference between knowing the path and walking the path.", "Wabbalubadubdub", "That's not how the Force works", "Lol"];

	app.get('/', function(req, res) {
		res.json({'quote': quotes[Math.floor(Math.random() * quotes.length)]});
		res.end();
	});

	app.post('/add', function(req, res) {
		var newQ = req.body.quote;
		console.log(newQ);
		quotes.push(newQ);
		res.json({'status': 'quote added'});
	});

	app.delete('/del/:num', function(req, res) {
		var index = req.params.num;
		if (index > -1) quotes.splice(index, 1);
		res.json({'status': 'quote deleted'});
	});
}


module.exports = appRouter;