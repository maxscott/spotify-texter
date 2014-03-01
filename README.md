spotify-texter
==============

"executer" used twilio for execution of arbitrary sql via sms + results in .csv format.
"get_messages" returned the messages for a given number and marked those read.
"get_twilio_number" fetched the next available registered number and marked it in usage.
"text_request" took a sent text message and entered it into the database for a given phone number. Squelching the f bomb for demo purposes...
