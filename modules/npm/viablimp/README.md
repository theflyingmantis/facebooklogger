# viablimp #

This is the logging library. "Viablimp" delivers you the data you send through it to your facebook account. You can find more information about Blimp's Public API documentation at [https://facebooklogger.herokuapp.com/](https://facebooklogger.herokuapp.com/).
If you have any problems or requests please contact [support](mailto:abhinav.rai.1996@gmail.com?subject=Viablimp Python library).


## License ##
Licensed under the MIT License.

## Install ##

Using npm:

```
npm install viablimp
```

## Pre-Usage ##

Before we begin you need to get the token by messaging [https://m.me/viablimp/](https://m.me/viablimp/).

## Usage ##

```javascript
let viablimp = require('viablimp');

let log = new viablimp('OLDQRKPW2A'); //Here OLDQRKPW2A is the token received
log.add_name('Testing')	//Useful when multiple services use logging.
let loggingObject = {'A': 1}

log.message(loggingObject).then(data=>{
	console.log(data);
}).catch(error=>{
	console.log(error);
})
// Sends the message to FB user whose token is 'OLDQRKWPW2A'. Visit https://m.me/viablimp to get your token.

log.message('Hey There')
```

## Improvements
What else would you like this library to do? Let me know. Feel free to send pull requests for any improvements you make.

### Todo
* Tests
* Warning and error messages
