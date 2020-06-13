#!/usr/bin/env python3

"""A client module for the socket echo. It reads data from the keyboard and
sends it to a server.
"""

import argparse
import socket
import sys
import os

parser = argparse.ArgumentParser(description='Echo Client')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    help='the server port number to connect to')
parser.add_argument("-m", "--machine", dest="host", type=str, default='localhost',
                    help="the server name or IP address to connect to")

options = parser.parse_args()

if options.port > 65536 or options.port <= 1500:
    print("Invalid port: the port number has to be between 1501 and 65536")
    exit(1)

connection_with_server = None

def handle_reception(server_socket, input_msg):

    try:

        # Receive the incoming message
        msg = server_socket.recv(1024)
        # If no data received
        # Return data
        if msg:
            print("\n" + msg.decode("utf-8") + "\n" + input_msg)     

    except:
        return("error")      



try:
    # Socket creation
    connection_with_server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # Connection with the server
    connection_with_server.connect((options.host,options.port))
    client_id=connection_with_server.recv(1)
    msg = "Client n°" + str(client_id.decode("utf-8")) + " type the string to send: (quit/exit to end) "
    child_pid = os.fork()
    if child_pid==0:
        while True:
            handle_reception(connection_with_server, msg)
    done = False
    while (not done):         
        inputString = input(msg).encode('utf-8')
        if inputString.decode("utf-8") in ("exit", "quit"):
            done = True
        else:
            connection_with_server.send(inputString)
    
    
        
        
            
            
# Interception of socket errors and interruption by the user (Ctrl-C)    
except(socket.error,KeyboardInterrupt) as se:
    # we're just going to print the exception
    print(se)
finally:
    if connection_with_server:
        connection_with_server.close()

print ("Ending ... \n")
exit(0)
