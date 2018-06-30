Viablimp ("Via Blimp")
--------

History
--------
	"Blimp" is a small airship or a barrage balloon. "Viablimp" delivers you the data you send through it to your facebook account.

What it Does
--------
	Blimp is a chatbot.
	Blimp provides you a unique URL when you message the bot.
	This unique url when hit with any data (GET/POST request) messages you the data in json on your fb account.
	Imagine this to be a wormhole! Anything you do with the url, the message is sent by you on your phone messenger account.
	Also can be used as a testing API endpoint.

Website
-------
https://facebooklogger.herokuapp.com/

Usage
--------
To use, simply do::

    >>> import viablimp
    >>> logger = viablimp.token('BGSFH3HJ7I') # The Token which you get from the viablimp facebook chatbot
    >>> logger.add_name('SERVICE_NAME') # Optional. Useful when multiple services use logging.
    >>> logger.message(STRING/OBJECT TO LOG)

