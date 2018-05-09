var csvStream = require('csv-write-stream');
var writer;

function CSV() {
     writer = csvStream({ headers: ["todo-item"]});
}

CSV.prototype.write = function(txt) {
    writer.pipe(fs.createWriteStream('todo-list.csv'))
    writer.write([txt])
    writer.end()
};

CSV.prototype.read = function() {
    fs.readFile('todo-list.csv', (err, data) => {
        if (err) throw err;
        console.log(data);
      });
};

module.exports = CSV;