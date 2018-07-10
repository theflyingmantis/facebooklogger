"use strict";
var request = require('request');

class viablimp{
	constructor(token) {
		this.token=token;
	}
	add_name(service) {
		this.service=service;
	}
	message(logObject) {
		logObject = JSON.stringify(logObject)
		return new Promise((resolve, reject) => {
		    if (!logObject) {
		      	reject('Enter anything to log. Eg. viablimp("Test-123")')
		    } 
		    else if (typeof logObject === 'function') {
		      	reject('¯\\_(ツ)_/¯')
		    } 
		    else {
		    	console.log('LOG:'+ new Date() +'\n'+logObject)
		    	if (!this.service){
		    		this.service="NO1";
		    	}
			    let options = {
			    	url: "https://facebooklogger.herokuapp.com/logging/"+this.service+"/"+this.token,
			    	headers: {
            			'content-type': 'application/json'
			    	},
			    	body: logObject
			    }
			    request.post(options, function(err,resp,body){
			    	if (resp.statusCode>=300 || resp.statusCode <200){
			    		reject('Wrong Token')
			    	}
			    	if (err){
			    		reject(err);
			    	}
			    	else{
			    		resolve(resp.statusCode);
			    	}
			    })
		    }
		})
	}
}


module.exports = viablimp;