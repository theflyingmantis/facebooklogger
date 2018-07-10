"use strict";
let viablimp = require('./'); // require the `index.js` file from the same directory.

let log = new viablimp('OLDQRKPW2A');
log.add_name('Testing')
let loggingObject = {'A': 1}

log.message(loggingObject).then(data=>{
	console.log(data);
}).catch(error=>{
	console.log(error);
})
// Sends the message to FB user whose token is 'OLDQRKWPW2A'. Visit https://m.me/viablimp to get your token.

log.message('Hey There')