var fs = require("fs");
console.log("Going to write into existing file");
// Open a new file with name cssmang.txt and write Light or Dark! to it.
fs.readFile('/home/daksh/Projects/flask-tutorial/flaskr/templates/cssmang.txt', function (err, data) {
    if (err) {
       return console.error(err);
    }
    let vsiv = data.toString()
 });

fs.writeFile('/home/daksh/Projects/flask-tutorial/flaskr/templates/cssmang.txt', 'Light', function(err) {
   if (err) {
      return console.error(err);
   } // Display any error in writing to file
   console.log("Data written successfully!"); // Show success message
   console.log("Let's read newly written data")
   // Read the newly written file and print all of its content on the console
   /*fs.readFile('../cssmang.txt', function (err, data) {
      if (err) {
         return console.error(err);
      }
      console.log("Asynchronous read: " + data.toString());
   }); */
});

fs.readFile('/home/daksh/Projects/flask-tutorial/flaskr/templates/cssmang.txt', function (err, data) {
    if (err) {
       return console.error(err);
    }
    let vsiv = data.toString()
 });
