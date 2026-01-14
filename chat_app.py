import socket
import sys
import threading
import tkinter as tk
from tkinter import simpledialog
stop_event = threading.Event()

######################################
#Creating a main window at the start
######################################

# Note to self:
# We start the main window and make very other window a child of it 
# This is best practice and ensures that when the main window dies so does the child windows 
# For example see line 23   (choice = simpledialog.askstring("Chat", "Host or connect? (1/2)", parent=mainWindow))
mainWindow = tk.Tk()
mainWindow.title('Chat')
mainWindow.withdraw()       #hides mainWindow


#Initializing socket & network connections
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
choice = simpledialog.askstring("Chat", "Host or connect? (1/2)", parent=mainWindow)

if choice == "1":
    ip = simpledialog.askstring("Chat", "Enter your IP:")
    port = int(simpledialog.askstring("Chat", "Enter your port:", parent=mainWindow))
    tk.messagebox.showinfo(title=None, message='Chat attempt starting - when connected a new window will appear', parent=mainWindow)  
    sock.bind((ip, port))
    sock.listen()
    print('waiting for connection')
    sock, address = sock.accept()
    print('connected')
    #continue to line 48 and onward
    
elif choice == "2":
    ip = simpledialog.askstring("Chat", "Enter server IP:", parent=mainWindow)
    port = int(simpledialog.askstring("Chat", "Enter server port:", parent=mainWindow))
    tk.messagebox.showinfo(title=None, message='Chat attempt starting', parent=mainWindow)  
    print('attempting connection')
    sock.connect((ip, port))
    print('connected')
    #continue to line 48 and onward
else:
    tk.messagebox.showerror(title=None, message='Not Acceptable', parent=mainWindow)
    sys.exit()

######################################
#GUI building and commands (functions)
######################################
mainWindow.deiconify()      #bring back mainWindow

#Chat window
chatWindow = tk.Text(mainWindow, state="disabled", height=20, width=50)
chatWindow.pack(padx=10, pady=10)

#Box to enter messages
enterMessages = tk.Entry(mainWindow)
enterMessages.pack()

#Sending messages
def sendMessage(event=None):                #only ran when command called (no need for seperate thread)
    message = enterMessages.get()
    enterMessages.delete(0, tk.END)         #delete eveything in the messagebox from index 0-tk.End()
    if message.lower() == 'exit':
        sock.send(message.encode())         #send exit message to peer
        stop_event.set()                    #set exit signal so recv thread stops
        return                              #finish function early (the sender of the exit signal will now have their own exit based on recv logic)
    try:
        if message:
            sock.send(message.encode())
            chatWindow.config(state='normal')
            chatWindow.insert(tk.END, f"You> {message}\n")
            chatWindow.config(state='disabled')
    except:
        tk.messagebox.showerror(title=None, message='Message Sending Error', parent=mainWindow)
        sock.close()
        mainWindow.destroy()
        sys.exit()
       
#Sending logic
sendButton = tk.Button(mainWindow, text="Send", command=sendMessage)
enterMessages.bind("<Return>", sendMessage) #pressing enter sends messages

#Recv messages
#Note to self: 
#Now we are dealing with threads so we must be careful
#When it comes to gui related actions we want to make sure we run it in the context of the mainWindow (tk) thread and not the recvThread
#For example -> mainWindow.after(0, lambda m=message: chatWindowInsert(m)) 
#This waits to run gui actions within the main thread
def recvMessage():                          #needs to be ran constantly and will need its own thread
    while not stop_event.is_set():          #while the signal is not set continue to recieve data
        try:
            data = sock.recv(1024)
            message = data.decode()
            if message.lower() == 'exit':
                #mainWindow.after(0, lambda: tk.messagebox.showerror(title=None, message='Partner disconnected', parent=mainWindow))
                mainWindow.after(0, on_closing)
                break
            mainWindow.after(0, lambda m=message: chatWindowInsert(m)) #calls from main thread
        except:
            mainWindow.after(0, lambda: tk.messagebox.showerror(title=None, message='Message Recv Error', parent=mainWindow))
            mainWindow.after(0, on_closing)
            break

def chatWindowInsert(text):
    chatWindow.config(state='normal')
    chatWindow.insert(tk.END, f"Partner> {text}\n") #Insert this text at the end of the widget’s current content
    chatWindow.config(state='disabled')

def on_closing():           
    try:
        #this function should already be executing in main thread context when called (see line 98)
        tk.messagebox.showerror(title=None, message='Partner disconnected', parent=mainWindow)
        stop_event.set()        # tell thread to stop
        sock.close()
        recvThread.join()       #main thread must now wait for recv thread to end in order to die
        mainWindow.destroy()    #destroy gui
    except:
        sys.exit()              #hard exit

recvThread = threading.Thread(target=recvMessage, daemon=True)          #a daemon is a background thread that does not keep the program running on its own (if daemon threads are the only ones alive python still exits!)
recvThread.start()
mainWindow.mainloop()
