# Python Multiplayer Game

A learning project for Python development fundamentals with real-time multiplayer functionality!

## 🎮 How to Play Multiplayer

### **Step 1: Install Dependencies**
```bash
# Activate virtual environment (if using one)
venv\Scripts\activate

# Install required packages
pip install websockets
```

### **Step 2: Start the Server (Host)**
**One person (the host) runs this:**
```bash
python server.py
```
This will show you the server IP address. Share this IP with your friend!

### **Step 3: Connect Players**
**Both players run this:**
```bash
python main.py
```

1. Enter your player name
2. Enter the server IP (the host can use "localhost")
3. Start chatting and playing!

## 🎯 Game Features

- **Real-time chat** - Type messages to talk to other players
- **Game actions** - Use `/action <description>` to perform game moves
- **Player notifications** - See when players join/leave
- **Network play** - Works over local network (same WiFi)

## 🎮 Commands

While connected:
- Type normally to **send chat messages**
- `/action <description>` - Perform a game action
- `/quit` - Leave the game

## 📡 Network Setup

### For Same Computer (Testing):
- Host: Use `localhost` or `127.0.0.1`
- Client: Use `localhost` or `127.0.0.1`

### For Same Network (Friends):
- Host: Run `python server.py` - it will show your IP address
- Client: Use the IP address shown by the server

### Example:
```
Host runs server.py and sees:
🌐 Server IP: 192.168.1.100
📡 Port: 8765
📋 Tell your friend to connect to: ws://192.168.1.100:8765

Friend enters: 192.168.1.100
```

## 🏗️ Technical Details

### Project Structure
```
pythonmultiplayergame/
├── server.py          # Game server (host runs this)
├── main.py            # Game client (players run this)
├── requirements.txt   # Dependencies
└── README.md         # This file
```

### What You'll Learn
- **WebSocket networking** - Real-time communication
- **Async programming** - Non-blocking code
- **JSON messaging** - Data exchange format
- **Threading** - Handling multiple tasks
- **Error handling** - Robust network code