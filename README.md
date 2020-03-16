# Flask PI Server
A [Flask](https://palletsprojects.com/p/flask/) webserver that takes HTTP requests and translates them into actions (PI commands) that are performed on the scope.  

## How to run
### Requirements
* Python 3
* [NI Visa (or equivalent software)](https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html#329456)
### Setup 
Once you've cloned the project, you'll need to setup your virtual environment ([the flask docs](https://flask.palletsprojects.com/en/1.1.x/installation/#virtual-environments) gives an explanation of what this is and how to set it up. Follow them through to the end of the page). You should show be inside of your virtual environment  

##### Install PyVisa:
```
pip install -U pyvisa
```  

##### Set environment variables:
FLASK_APP = "flaskr"  
FLASK_ENV = "development"  

##### Start the server
```
flask run
```
Optionally supply the ```--host=0.0.0.0``` argument if you want to server to accessible from other devices (such as if you're using a certain remote scope control app 🤔)

## How to use
### Connect the server to the scope
Before you can start sending commands to the scope, first you'll need to make sure that the server is talking with the scope. This can be down by sending a HTTP POST method to ```/connect``` with a parameter called ```ip``` that has the IP of the scope you want to interact with.

### Start sending commands.
Now you can start sending commands! This is also done by POST methods. The request should be sent to ```/command```. At minimum you'll need to supply one parameter ```command``` that is the name of the command to execute. You'll also need to include any parameters that are required for the command. The list of supported commands and their parameters (the names are surrounded by "$") are located in the ```createCommandDict()``` function.  
Parameter values currently correspond to whatever value the underlying PI command expects.
