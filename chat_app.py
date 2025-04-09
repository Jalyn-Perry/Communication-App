import socket
import threading
import rsa
import sys

"""
TODO
Usernames/Nicknames: Allow users to set a username so messages display as username: message instead of just "You" or "partner".
Command Support: Implement special commands like /exit to leave the chat, /clear to clear the screen, or /help for a list of commands.
Timestamps: Display timestamps for messages.
File sending
"""

### act 1

"""
how communication works
Server Setup:

When the server part of the code is run (by choosing option 1), it creates a TCP socket, binds it to the specified IP (you can use 127.0.0.1 for the local machine), and starts listening for incoming connections on port 1122.
Client Setup:

When the client part of the code is run (by choosing option 2), it creates another TCP socket and connects to the specified IP and port (127.0.0.1:1122).
Two Different Windows:

Run the program in two separate terminal or command windows.
In one window, choose 1 to start the server.
In the other window, choose 2 to start the client and connect to the server.
"""

choice = int(input("Do you want to host or connect... 1 or 2:\t"))

if choice == 1:
    yourIP = input("Enter your ip:\t")
    server =socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a tcp socket
    server.bind((yourIP, 4433)) #create a server here
    server.listen() #listen for a single connection
    print("listening...")
    client, _ = server.accept() #client is assigned the new connection (discards unneccesary stuff)
    print("partner has joined...\n")
elif choice ==2:
    theirIP = input("Enter IP to connect to:\t")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a tcp socket
    client.connect((theirIP, 4433)) #connect
    print("connection successful\n")
else:
    exit()
    

#### sending messages through socket
def sendMessage(client):
    while True:
        try:
            message = input("")
            if message == "exit":                
                client.send(message.encode())
                print("exit message sent to peer.. closing connection")
                client.close()
                sys.exit()
            else:
                client.send(message.encode())
                print("You: "+ message )
        except:
            print("connection no longer established-> chat exited -> closing sending process")
            break
        
#### recving messages through socket
def recvMessage(client):
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg =="exit":
                print("exit request recieved... from peer")
                sys.exit()   
        except:
            print("connection no longer established-> chat exited -> closing recv process")
            break
        else:
            print("partner>  " + msg)
        
        
        

## threading
#each line below basically starts a function and passes args
#when the entire code is run, all 3 sections of code are ran at once
threading.Thread(target=sendMessage, args=(client,)).start()
threading.Thread(target=recvMessage, args=(client,)).start()








"""
threading.Thread:

This creates a new thread.
The Thread class from the threading module is used to initialize and run a thread.
Parameters:

target: The function that the thread will execute.
args: A tuple of arguments to pass to the target function.
.start():

This method starts the thread, running the target function in parallel with the main program.

These two threads (sendMessage and recvMessage) run simultaneously and independently of the main thread.
This allows the program to send and receive messages concurrently, improving responsiveness.

each user has a sending thread and receving thread, both must be closed in order to exit.
"""