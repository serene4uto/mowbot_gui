import asyncio
import websockets
import json
import struct


class FoxgloveClient:
    SUPPORTED_SUBPROTOCOL = "foxglove.websocket.v1"

    def __init__(self, uri):
        self.uri = uri
        self.ws = None
        self.event_handlers = {}
        self.channels = {}  # Store available channels

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
                # Handle binary message
                # self.handle_binary_message(message)
                pass
            else:
                # Handle JSON message
                parsed_message = json.loads(message)
                print(f"Received JSON message: {parsed_message}")

                # Trigger events based on the "op" field
                op = parsed_message.get("op")
                if op:
                    self.trigger_event(op, parsed_message)

                # Handle advertised channels
                if op == "advertise":
                    await self.handle_advertised_channels(parsed_message)
        except Exception as e:
            print(f"Error processing message: {e}")
            self.trigger_event("error", e)

    def handle_binary_message(self, message):
        """
        Decode and print binary messages.
        Format: subscriptionId (4 bytes), timestamp (8 bytes), payload (remaining bytes).
        """
        try:
            # Decode subscriptionId and timestamp
            subscription_id, timestamp = struct.unpack_from("<Iq", message, offset=0)
            payload = message[12:]  # Remaining bytes are the payload

            print(f"Streaming message received:")
            print(f"  Subscription ID: {subscription_id}")
            print(f"  Timestamp: {timestamp}")
            print(f"  Payload (raw): {payload}")

            # Attempt to decode the payload as JSON (if applicable to the schema)
            try:
                decoded_payload = json.loads(payload.decode("utf-8"))
                print(f"  Payload (decoded as JSON): {decoded_payload}")
            except Exception as e:
                print(f"  Could not decode payload as JSON: {e}")
        except Exception as e:
            print(f"Error decoding binary message: {e}")

    async def handle_advertised_channels(self, message):
        """
        Subscribe to all advertised channels.
        """
        channels = message.get("channels", [])
        print(f"Received advertised channels: {channels}")
        for channel in channels:
            channel_id = channel["id"]
            if channel_id not in self.channels:
                self.channels[channel_id] = channel
                print(f"New channel advertised: {channel}")

                # Subscribe to the channel
                await self.send({
                    "op": "subscribe",
                    "subscriptions": [
                        {"id": channel_id, "channelId": channel_id}
                    ]
                })
                print(f"Subscribed to channel: {channel_id}")

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
    client.on("advertise", lambda message: print(f"Channels advertised: {message}"))
    client.on("message", lambda message: print(f"Streamed message: {message}"))

    # Connect to the server
    await client.connect()

# Run the client
asyncio.run(main())
