#!/usr/bin/env python3
"""
Python Multiplayer Game - Client
Players run this to connect to the game server
"""

import asyncio
import websockets
import json
import threading
import sys

class GameClient:
    def __init__(self):
        self.websocket = None
        self.connected = False
        self.player_name = ""
    
    async def connect_to_server(self, server_ip, player_name):
        """Connect to the game server"""
        try:
            self.websocket = await websockets.connect(f"ws://{server_ip}:8765")
            self.connected = True
            self.player_name = player_name
            
            # Send join message
            await self.websocket.send(json.dumps({
                "type": "join",
                "name": player_name
            }))
            
            print(f"✅ Connected to server as '{player_name}'!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            return False
    
    async def listen_for_messages(self):
        """Listen for messages from the server"""
        try:
            async for message in self.websocket:
                data = json.loads(message)
                await self.handle_server_message(data)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Disconnected from server")
            self.connected = False
        except Exception as e:
            print(f"❌ Error listening for messages: {e}")
            self.connected = False
    
    async def handle_server_message(self, data):
        """Handle messages received from server"""
        message_type = data.get("type", "")
        
        if message_type == "welcome":
            print(f"🎮 {data['message']}")
            print(f"👥 Players in game: {data['players_count']}")
        
        elif message_type == "player_joined":
            print(f"🎉 {data['message']}")
            print(f"👥 Total players: {data['players_count']}")
        
        elif message_type == "player_left":
            print(f"👋 {data['message']}")
            print(f"👥 Remaining players: {data['players_count']}")
        
        elif message_type == "chat":
            if data['player'] != self.player_name:  # Don't show our own messages
                print(f"💬 {data['player']} ({data['timestamp']}): {data['message']}")
        
        elif message_type == "game_action":
            if data['player'] != self.player_name:  # Don't show our own actions
                print(f"🎮 {data['player']} {data['action']} ({data['timestamp']})")
    
    async def send_chat_message(self, message):
        """Send a chat message to all players"""
        if self.connected:
            await self.websocket.send(json.dumps({
                "type": "chat",
                "message": message
            }))
    
    async def send_game_action(self, action):
        """Send a game action to all players"""
        if self.connected:
            await self.websocket.send(json.dumps({
                "type": "game_action",
                "action": action
            }))

def get_user_input(client):
    """Handle user input in a separate thread"""
    while client.connected:
        try:
            user_input = input()
            if user_input.startswith("/"):
                # Commands start with /
                if user_input == "/quit":
                    client.connected = False
                    break
                elif user_input.startswith("/action "):
                    action = user_input[8:]  # Remove "/action "
                    asyncio.run_coroutine_threadsafe(
                        client.send_game_action(action), 
                        client.loop
                    )
                else:
                    print("Commands: /quit, /action <action>")
            else:
                # Regular chat message
                asyncio.run_coroutine_threadsafe(
                    client.send_chat_message(user_input), 
                    client.loop
                )
        except EOFError:
            break
        except Exception as e:
            print(f"Error with input: {e}")
            break

async def main():
    """Main game client"""
    print("🎮 PYTHON MULTIPLAYER GAME CLIENT")
    print("=" * 40)
    
    # Get player name
    player_name = input("Enter your player name: ").strip()
    if not player_name:
        print("❌ Player name cannot be empty!")
        return
    
    # Get server IP (default to localhost for testing)
    print("\n🌐 SERVER CONNECTION")
    server_ip = input("Enter server IP (press Enter for localhost): ").strip()
    if not server_ip:
        server_ip = "localhost"
    
    # Create client and connect
    client = GameClient()
    client.loop = asyncio.get_event_loop()
    
    if await client.connect_to_server(server_ip, player_name):
        print("\n💬 GAME CHAT (type messages to chat)")
        print("📝 Commands:")
        print("   - Type normally to send chat messages")
        print("   - /action <description> - Perform a game action")
        print("   - /quit - Leave the game")
        print("=" * 40)
        
        # Start input thread
        input_thread = threading.Thread(
            target=get_user_input, 
            args=(client,), 
            daemon=True
        )
        input_thread.start()
        
        # Listen for server messages
        await client.listen_for_messages()
    
    print("👋 Thanks for playing!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Game closed by user")