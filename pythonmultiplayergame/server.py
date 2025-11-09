#!/usr/bin/env python3
"""
Multiplayer Game Server
Host runs this to create the game room
"""

import asyncio
import websockets
import json
from datetime import datetime

class GameServer:
    def __init__(self):
        # Store all connected players
        self.players = {}  # {websocket: player_info}
        self.game_state = {
            "players_count": 0,
            "messages": [],
            "game_started": False
        }
    
    async def register_player(self, websocket, player_name):
        """Add a new player to the game"""
        self.players[websocket] = {
            "name": player_name,
            "joined_at": datetime.now().strftime("%H:%M:%S")
        }
        self.game_state["players_count"] = len(self.players)
        
        print(f"✅ Player '{player_name}' connected! Total players: {len(self.players)}")
        
        # Send welcome message to the new player
        await self.send_to_player(websocket, {
            "type": "welcome",
            "message": f"Welcome {player_name}! You're connected to the game.",
            "players_count": len(self.players)
        })
        
        # Notify all other players
        await self.broadcast_to_others(websocket, {
            "type": "player_joined",
            "message": f"{player_name} joined the game!",
            "players_count": len(self.players)
        })
    
    async def unregister_player(self, websocket):
        """Remove a player from the game"""
        if websocket in self.players:
            player_name = self.players[websocket]["name"]
            del self.players[websocket]
            self.game_state["players_count"] = len(self.players)
            
            print(f"❌ Player '{player_name}' disconnected! Remaining players: {len(self.players)}")
            
            # Notify remaining players
            await self.broadcast_to_all({
                "type": "player_left",
                "message": f"{player_name} left the game.",
                "players_count": len(self.players)
            })
    
    async def send_to_player(self, websocket, message):
        """Send message to a specific player"""
        try:
            await websocket.send(json.dumps(message))
        except websockets.exceptions.ConnectionClosed:
            pass
    
    async def broadcast_to_all(self, message):
        """Send message to all connected players"""
        if self.players:
            disconnected = []
            for websocket in self.players:
                try:
                    await websocket.send(json.dumps(message))
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(websocket)
            
            # Clean up disconnected players
            for websocket in disconnected:
                await self.unregister_player(websocket)
    
    async def broadcast_to_others(self, sender_websocket, message):
        """Send message to all players except the sender"""
        for websocket in self.players:
            if websocket != sender_websocket:
                await self.send_to_player(websocket, message)
    
    async def handle_player_message(self, websocket, message_data):
        """Handle messages from players"""
        player_name = self.players[websocket]["name"]
        message_type = message_data.get("type", "")
        
        if message_type == "chat":
            # Broadcast chat message to all players
            chat_message = {
                "type": "chat",
                "player": player_name,
                "message": message_data["message"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            await self.broadcast_to_all(chat_message)
            print(f"💬 {player_name}: {message_data['message']}")
        
        elif message_type == "game_action":
            # Handle game actions (like moves, attacks, etc.)
            action_message = {
                "type": "game_action",
                "player": player_name,
                "action": message_data["action"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            await self.broadcast_to_all(action_message)
            print(f"🎮 {player_name} performed action: {message_data['action']}")
    
    async def handle_player_connection(self, websocket):
        """Handle new player connections"""
        try:
            # Wait for player to send their name
            initial_message = await websocket.recv()
            data = json.loads(initial_message)
            
            if data["type"] == "join" and "name" in data:
                await self.register_player(websocket, data["name"])
                
                # Listen for messages from this player
                async for message in websocket:
                    try:
                        message_data = json.loads(message)
                        await self.handle_player_message(websocket, message_data)
                    except json.JSONDecodeError:
                        if websocket in self.players:
                            print(f"Invalid message from {self.players[websocket]['name']}")
            
        except websockets.exceptions.ConnectionClosed:
            pass
        except json.JSONDecodeError:
            print("Invalid join message received")
        finally:
            await self.unregister_player(websocket)

# Start the game server
async def start_server():
    game_server = GameServer()
    
    # Get the local IP address for the network
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("🎮 MULTIPLAYER GAME SERVER STARTING...")
    print(f"🌐 Server IP: {local_ip}")
    print(f"📡 Port: 8766")
    print(f"📋 Tell your friend to connect to: ws://{local_ip}:8766")
    print("=" * 50)
    
    # Start the WebSocket server directly with the bound method
    server = await websockets.serve(
        game_server.handle_player_connection,
        "0.0.0.0", 
        8766
    )
    
    print("✅ Server is running! Waiting for players...")
    print("Press Ctrl+C to stop the server")
    
    await server.wait_closed()

if __name__ == "__main__":
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")