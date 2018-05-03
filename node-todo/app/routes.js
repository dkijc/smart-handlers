var Todo = require('./models/todo');
const uuid4 = require('uuid/v4');
var PORT = 5005;
var HOST = '127.0.0.1';

var dgram = require('dgram');

var obj = {
    table: []
 };

function getTodos(res) {
    var fs = require('fs');
    if (fs.existsSync('todo-list.json')) {
        fs.readFile('todo-list.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
                let parsedJson = JSON.parse(data)['table'];
                if(res) {
                    res.json(parsedJson);
                }
            }
        });    
    }
};

module.exports = function (app) {
    // api ---------------------------------------------------------------------
    // get all todos
    app.get('/api/todos', function (req, res) {
        // use mongoose to get all todos in the database
        getTodos(res);
    });

    // create todo and send back all todos after creation
    app.post('/api/todos', function (req, res) {
        obj.table.push({id: uuid4(), description:req.body.text});
        var json = JSON.stringify(obj);
        var fs = require('fs');
        
        if (fs.existsSync('todo-list.json')) {
            fs.readFile('todo-list.json', 'utf8', function readFileCallback(err, data){
                if (err){
                    console.log(err);
                } else {
                obj = JSON.parse(data); //now it an object
                obj.table.push({id: uuid4(), description: req.body.text}); //add some data
                json = JSON.stringify(obj); //convert it back to json
                fs.writeFile('todo-list.json', json, 'utf8', function (err) {
                    if (err) {
                        console.log("[Update Error]: " + err);
                    } else {
                        console.log("Recieved Data: " + req.body.text);
                        getTodos(res);
                        var client = dgram.createSocket('udp4');
                        var message = new Buffer(req.body.text);

                        client.send(message,PORT, HOST, function(err) {
                            if (err) throw err;
                            console.log('UDP message sent to ' + HOST +':'+ PORT);
                            client.close();
                        });
                    }
                }); // write it back 
            }});    
        } else {
            fs.writeFile('todo-list.json', json, 'utf8', function (err) {
                if (err) {
                    console.log("[Write Error]: " + err);
                } else {
                    console.log("Recieved Data: " + req.body.text);
                    getTodos(res);
                    
                    var client = dgram.createSocket('udp4');
                    var message = new Buffer(req.body.text);

                    client.send(message,PORT, HOST, function(err) {
                        if (err) throw err;
                        console.log('UDP message sent to ' + HOST +':'+ PORT);
                        client.close();
                    });
                }
            });
        }
    });

    // delete a todo
    app.delete('/api/todos/:todo_id', function (req, res) {
        var fs = require('fs');
        fs.readFile('todo-list.json', 'utf8', function readFileCallback(err, data){
            if (err){
                console.log(err);
            } else {
                let list = JSON.parse(data)['table'];
                for (i in list) {
                    if (req.params.todo_id === list[i].id) {
                        if (i > -1) {
                            list.splice(i, 1);
                            obj = { 
                                "table": list
                            };

                            json = JSON.stringify(obj); //convert it back to json

                            fs.writeFile('todo-list.json', json, 'utf8', function (err) {
                                if (err) {
                                    console.log("[Update Error]: " + err);
                                } else {
                                    getTodos(res);
                                    console.log("Deleted Id: " + req.params.todo_id);
                                    var client = dgram.createSocket('udp4');
                                    var message = new Buffer(req.params.todo_id);
                                    
                                    client.send(message,PORT, HOST, function(err) {
                                        if (err) throw err;
                                        console.log('UDP message sent to ' + HOST +':'+ PORT);
                                        client.close();
                                    });
                                }
                            }); // write it back 
                        }
                    }
                }
            }
        });    
    });

    // application -------------------------------------------------------------
    app.get('*', function (req, res) {
        res.sendFile(__dirname + '/public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
    });
};
