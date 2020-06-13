#!/usr/bin/python3
"""A client module for the socket echo. It reads data from the keyboard and
sends it to a server.
"""
import select, socket, sys, argparse

parser = argparse.ArgumentParser(description='Echo Server')
parser.add_argument('-p', '--port', dest='port', type=int, default=1800,
                    help='the port number to bind to')

options = parser.parse_args()

if options.port > 65536 or options.port <= 1500:
    print("Invalid port: the port number has to be between 1501 and 65536")
    exit(1)

host = 'localhost'  # default is localhost ("127.0.0.1)
port=options.port

# Creation of a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind to use given host and port
server.bind((host,port))

# Ready to listen for clients
server.listen()

# List of sockets
sockets_input_list = [server]

# List of connected clients
clients = {}

print("Server on listening on --> " + str(host) + ":" + str(port))

def handle_client(client_socket):

    try:

        # Receive the incoming message
        msg = client_socket.recv(1024)
        # If no data received
        if not msg:
            return False
        msg="Client n°" + str(clients[client_socket]) + " --> " + msg.decode("utf-8")
        # Return data
        return(msg)     

    except:
        return ("error")       
try:
    nb_of_clients = 0
    while sockets_input_list:
         
        readable_sockets, writable_sockets, exceptional_sockets = select.select(sockets_input_list, [] , sockets_input_list)
        
        for incoming_socket in readable_sockets:

            if incoming_socket is server:
    
                # Server accept connection with client
                client_socket, client_address = server.accept()
                # Add client_socket to select.select() list
                sockets_input_list.append(client_socket)
                nb_of_clients = nb_of_clients+1
                clients[client_socket]=nb_of_clients
                client_socket.send(str(nb_of_clients).encode("utf-8"))
                print("New connection accepted --> " + str(nb_of_clients) + " Client(s) connected")
    
            # If a socket is an already existing connection, then read the incoming message
            else:
                data_recv=handle_client(incoming_socket)
                if data_recv:       
                    print("Forwarded message: " + data_recv)          
                    for client_socket in clients:              
                        if client_socket is not incoming_socket:
                            client_socket.send(data_recv.encode("utf-8"))
                            
        
# Interception of socket errors and interruption by the user (Ctrl-C)    
except(socket.error,KeyboardInterrupt) as se:
    # we're just going to print the exception
    print(se)
finally:
    if server:
        server.close()

print ("Ending ... \n")
exit(0)        

