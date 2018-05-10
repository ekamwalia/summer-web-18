var express = require('express')
var app = express()
var bodyParser = require('body-parser')

app.use(bodyParser.json())

var q = ['i dont know what half of these methods even mean', 'my god this is confusing', 'it was a poorly calculated decision to start with node']

app.get('/quotes', (req,res)=>{
	var a = Math.floor(Math.random()*q.length)
	res.json({'Quote ->' : q[a]})
	res.end()
})

app.delete('/delete/:id',(req,res)=>{
	var i = req.params.id -1
	q.splice(i,1)
	res.json({'message' : 'Quote deleted!'})
})

app.post('/add', (req,res)=>{
	q.push(req.body.quote)
	res.json({'message' : 'Quote added'})
})

app.listen(3000,(console.log('Sounds good')))