# Python TCP Chat

A simple **encrypted chat application** in Python using TCP sockets and threading.  
Allows two users to send and receive messages in real-time over a local network or the internet.  

> **Note:** This is for educational purposes. The author is **not responsible** for any misuse of this code.

---

## Features

- Real-time GUI chat between two users
- Separate **send** and **receive** functions for smooth messaging
- Simple command handling:
  - Type `exit` to close the connection gracefully
- Easy server/client setup via GUI

---

## Upcoming Features (TODO)

- Usernames / Nicknames
- Timestamps for messages
- Custom commands (`/exit`, `/clear`, `/help`)
- File transfer support
- End-to-end encryption using RSA or other crypto

---

## How It Works

### Server Setup

1. Run the script and choose `1` to start the server.
2. Enter the IP address to bind the server to (use `127.0.0.1` for local testing).
3. The server listens on port `4433` for incoming connections.
4. Wait for a client to connect.

### Client Setup

1. Run the script and choose `2` to start the client.
2. Enter the server’s IP address to connect.
3. Once connected, you can send and receive messages in real-time.

### Two Windows Required

- Open **two terminal windows**.
  - One for the server
  - One for the client

---

## Running the Chat

```bash
python chat.py
