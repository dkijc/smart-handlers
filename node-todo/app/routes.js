var Todo = require('./models/todo');
const uuid4 = require('uuid/v4');

var obj = {
    table: []
 };

function getTodos(res) {
    var fs = require('fs');
    fs.readFile('todo-list.json', 'utf8', function readFileCallback(err, data){
        if (err){
            console.log(err);
        } else {
            console.log(JSON.parse(data)['table']);
            res.json(JSON.parse(data)['table']);
        }
    });    
    // Todo.find(function (err, todos) {

    //     // if there is an error retrieving, send the error. nothing after res.send(err) will execute
    //     if (err) {
    //         res.send(err);
    //     }

    //     res.json(todos); // return all todos in JSON format
    // });
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
                        console.log("Recieved Data: " + req.body.text)
                        getTodos(res)
                    }
                }); // write it back 
            }});    
        } else {
            fs.writeFile('todo-list.json', json, 'utf8', function (err) {
                if (err) {
                    console.log("[Write Error]: " + err);
                } else {
                    console.log("Recieved Data: " + req.body.text)
                    getTodos(res)
                }
            });
        }

        // // create a todo, information comes from AJAX request from Angular
        // Todo.create({
        //     text: req.body.text,
        //     done: false
        // }, function (err, todo) {
        //     if (err)
        //         res.send(err);

        //     // get and return all the todos after you create another
        //     getTodos(res);
        // });

    });

    // delete a todo
    app.delete('/api/todos/:todo_id', function (req, res) {
        Todo.remove({
            _id: req.params.todo_id
        }, function (err, todo) {
            if (err)
                res.send(err);

            getTodos(res);
        });
    });

    // application -------------------------------------------------------------
    app.get('*', function (req, res) {
        res.sendFile(__dirname + '/public/index.html'); // load the single view file (angular will handle the page changes on the front-end)
    });
};
