import os
import visa
import re

from flask import Flask, request


#
#  Represents an instrument that one can connect and send commands to
#
class Instrument(object):
    def __init__(self):
        self.instrument = None
        self.ip = ""
        self.rm = visa.ResourceManager()

    # Connect to the scope at the given IP
    def connect(self, ip):
        self.ip = ip
        resourceName = "TCPIP::" + self.ip + "::INSTR"
        self.instrument = self.rm.open_resource(resourceName)

    # sends a command to the instrument
    def sendCommand(self, command):
        if (self.instrument != None):
            try:
                queryResult = ""
                # We want to return the result of query commands
                if ("?" in command):
                    queryResult = self.instrument.query(command)
                else:
                    self.instrument.query(command)
            except visa.VisaIOError as e:
                queryResult = "There was a timeout, verify on scope"
            # self.instrument.query('DISplay:GLObal:CH2:STATE OFF')
        # IF we're not conencted to a scope, say as much
        else:
            queryResult = "not connected to a scope"

        return queryResult


#
# Creates a dictionary with all the commands currently supported by this server
#
def createCommandDict():
    commands = dict()

    commands['getDisplayState'] = 'DISPLAY?'

    # Channel state
    commands['setChannelState'] = 'DISplay:GLObal:CH$ch_num$:STATE $state$'
    commands['getChannelState'] = 'DISplay:GLObal:CH$ch_num$:STATE?'

    return commands

# Takes the given command and params, and gets it ready to be sent to the scope
def parseCommand(command, params):
    # m = re.search(r'\$(.+?)\$', command)
    # m.
    pattern = re.compile(r'\$(.+?)\$')
    tokens = re.findall(pattern, command)

    # for every token in the command, replace it with the value from the params
    for token in tokens:
        tokenWithDelimiters = "$" + token + "$"
        if token in params:
            command = command.replace(tokenWithDelimiters, params[token])

    return command

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    my_instrument = Instrument()

    commands = createCommandDict()

    # a simple page that says hello
    @app.route('/hello')
    def hello():

        # TCPIP::10.233.69.194::port::SOCKET
        # TCPIP::10.233.69.194::INSTR
        # print(my_instrument.query('*IDN?'))
        # print("hello world!")
        # my_instrument.query('DISplay:GLObal:CH2:STATE OFF')
        return "hello"

    # Connects to a scope
    @app.route('/connect', methods=['POST'])
    def connect():
        response = ""
        if request.method == 'POST':
            # First, validate that the proper parameters were sent
            if ('ip' in request.form):
                # connect to the scope
                my_instrument.connect(request.form['ip'])
                respone = "connected"
                print("yippie")
            else:
                response = "You must supply the parameter ip, with the ip of the scope"

        return response

    # Issues a command to the scope
    @app.route('/command', methods=['GET', 'POST'])
    def command():
        response = ""
        # print(request.form)
        # return request.form
        # response = my_instrument.sendCommand(
        #     'DISplay:GLObal:CH2:STATE OFF')
        if 'command' in request.form:
            # Map the REST command to a PI command
            restCommand = request.form['command']
            if restCommand in commands:
                piCommand = commands[restCommand]
                # print(piCommand)
                # Replace the tokens in the command with the parameters supplied in the request
                parsedCommand = parseCommand(piCommand, request.form)
                print(parsedCommand);
                response = my_instrument.sendCommand(parsedCommand)
                # response = piCommand

            # Invalid command given
            else:
                response = "command not found"
        else:
            response = "You must supply the parameter 'command', with the command to send"

        return response


    return app
