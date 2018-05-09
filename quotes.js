var express = require("express");
var bodyParser = require("body-parser");
var routes = require("./routes.js")
var app = express();

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

routes(app);

var server = app.listen(3000, function () {
    console.log("app running on https://localhost:", server.address().port);
});