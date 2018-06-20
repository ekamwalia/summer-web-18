document.onload(() => {
	
});

function star(data) {
	var xhr = new XMLHttpRequest();
	xhr.open('POST', '/star');

	xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	xhr.send(JSON.stringify(data));
	console.log(this);
}