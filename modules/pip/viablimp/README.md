# viablimp #

This is the logging library. "Viablimp" delivers you the data you send through it to your facebook account. You can find more information about Blimp's Public API documentation at [https://facebooklogger.herokuapp.com/](https://facebooklogger.herokuapp.com/).
If you have any problems or requests please contact [support](mailto:abhinav.rai.1996@gmail.com?subject=Viablimp Python library).


## License ##
Licensed under the MIT License.

## Install ##

Using pip:

```
pip install viablimp
```

Using easy_install:

```
easy_install viablimp
````

## Pre-Usage ##

Before we begin you need to get the token by messaging [https://m.me/viablimp/](https://m.me/viablimp/).

## Usage ##

```python
import viablimp

# The Token which you get from the viablimp facebook chatbot
logger = viablimp.token('BGSFH3HJ7I') 

# Useful when multiple services use logging.
logger.add_name('SERVICE_NAME')

logger.message(STRING/OBJECT TO LOG) 
```

## Improvements
What else would you like this library to do? Let me know. Feel free to send pull requests for any improvements you make.

### Todo
* Tests
* Warning and error messages
