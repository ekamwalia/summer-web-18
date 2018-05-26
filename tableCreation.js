var mysql = require("mysql");
var connection = mysql.createConnection({
	host:'localhost',
	user:'root',
	password:'lolseeyou123',
	database: 'summer_web_project'
});

connection.connect();

connection.query("CREATE TABLE songs ( id INT AUTO_INCREMENT, title VARCHAR(100), rating INT, PRIMARY KEY(id));", (err,result)=>{
	if(err)
		console.log("Error:"+err);
	else
		console.log(result);
});