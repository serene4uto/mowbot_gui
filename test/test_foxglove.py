import asyncio
import websockets
import json

class FoxgloveClient:
    SUPPORTED_SUBPROTOCOL = "foxglove.websocket.v1"

    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self.event_handlers = {}

    async def connect(self):
        try:
            # Establish WebSocket connection with the required subprotocol
            self.ws = await websockets.connect(self.uri, subprotocols=[self.SUPPORTED_SUBPROTOCOL])
            print("Connected to the server")

            # Trigger the open event
            self.trigger_event("open")

            # Listen for incoming messages
            await self.listen()
        except Exception as e:
            print(f"Error during connection: {e}")
            self.trigger_event("error", e)

    async def listen(self):
        try:
            async for message in self.ws:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"Connection closed: {e}")
            self.trigger_event("close", e)

    async def handle_message(self, message):
        try:
            if isinstance(message, bytes):
                # Handle binary message if needed
                pass
            else:
                parsed_message = json.loads(message)
                print(f"Received message: {parsed_message}")

                # Trigger events based on the "op" field
                op = parsed_message.get("op")
                if op:
                    self.trigger_event(op, parsed_message)
        except Exception as e:
            print(f"Error processing message: {e}")
            self.trigger_event("error", e)

    async def send(self, message):
        try:
            if self.ws:
                await self.ws.send(json.dumps(message))
                print(f"Sent message: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
            self.trigger_event("error", e)

    def on(self, event_name, handler):
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        self.event_handlers[event_name].append(handler)

    def trigger_event(self, event_name, *args):
        handlers = self.event_handlers.get(event_name, [])
        for handler in handlers:
            handler(*args)

    async def close(self):
        if self.ws:
            await self.ws.close()
            print("Connection closed")


# Example usage
async def main():
    uri = "ws://localhost:8765"  # Replace with your WebSocket server URL

    # Initialize FoxgloveClient
    client = FoxgloveClient(uri)

    # Define event handlers
    client.on("open", lambda: print("Connection opened"))
    client.on("error", lambda error: print(f"Error: {error}"))
    client.on("close", lambda event: print("Connection closed"))
    client.on("serverInfo", lambda info: print(f"Server Info: {info}"))

    # Connect to the server
    await client.connect()

    # Send a test message (example for subscribe operation)
    # await client.send({
    #     "op": "subscribe",
    #     "subscriptions": [
    #         {"id": 1, "channelId": 123}  # Replace with actual IDs
    #     ]
    # })

# Run the client
asyncio.run(main())
