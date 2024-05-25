# IT6

modules needed:
unittest, api, flask_testing, flask, json, flask_mysqldb, dicttoxml, datetime, PyJWT

Description:

- This program is a python project, a CRUD REST API that connects to a specific database (hobbiespasstime) which it can then modify or view. It has functions of CRUD, search, JWT security, and user login. Output can be viewed as json or xml, with json being default.

Installation

- To install and initialize this project, you need first install all modules needed, you can install the modules in an environemnt or globally, once this is done, you can then use any pyhton interpreter to run the api.py and MySQL workbench to view the hobbies&passtime database.

Usage

- The web application is accesible to its host, to gain access however you must first log in and claim a token ID valid for one day. The username is <root> and the password is <root>, once you have recieved the message of a sucessful log in you can proceed to explore the other routues. In postman, you can log in by using the POST method and inputting the username and password on the form data field. If you wish to return your authorization, user can simply log out.

log in: http://127.0.0.1:5000/
log out: http://127.0.0.1:5000/logout

- To view the contents of the database, just go to specified route, do this by typing the additional words after http://127.0.0.1:5000/, the routes you can go tot are: events, members, hobbies_and_pasttime, organizations, and memberships. You can view individual instances by adding their UID after their table

view member: http://127.0.0.1:5000/members/15

- To use CRUD functions, simply add to the route dependeing on what exactly you would want to do: /add to POST, /update/<id> to PUT, and /del/<id> to DELETE

delete member: http://127.0.0.1:5000/members/del/15

- To change the output format of your request, simply add ?format=<xml/json>

xml format: http://127.0.0.1:5000/events?format=xml

You can run this program using POSTMAN and it is recommended to do so