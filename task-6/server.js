const express = require('express');
const session = require('express-session');	
const bodyParser = require('body-parser');

const routes = require('./routes');

const app = express();

// MIDDLEWARES //

app.use(express.json());
app.use(express.urlencoded({
	extended: true
}));

// TODO: Add session
app.use(session({
	secret: 'Cheeki Breeki Iv Damke',
	resave: false,
	saveUninitialized: true,
	cookie: { secure: false }
}));

// ROUTERS //

app.use(routes);
app.use(express.static('public'));

// APP SETTINGS //

app.set('view engine', 'pug');

app.listen(4200, (err) => {
	if (err) {
		console.log('Failed to start app: ' + err);
		return;
	} 
	console.log('Server listening at port 4200');
});
