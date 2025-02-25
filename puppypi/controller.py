import json
import websocket
import threading

# Replace with your PuppyPi IP
PUPPYPI_IP = "192.168.0.37"

# WebSocket URL (rosbridge default is ws://<PuppyPi-IP>:9090)
WEBSOCKET_URL = f"ws://{PUPPYPI_IP}:9090"

def on_message(ws, message):
    print("Received message: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("Closed")

def on_open(ws):
    # Create the request to call the service
    payload = {
        "op": "call_service",
        "service": "/puppy_control/runActionGroup",
        "args": {
            "name": "pee.d6ac",   # Action name: "sit"
            "wait": True      # Wait for completion: True
        }
    }
    
    # Send the payload as JSON
    ws.send(json.dumps(payload))

def call_puppy_service():
    # Create the WebSocket connection
    ws = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )
    
    # Start the WebSocket in a separate thread
    ws_thread = threading.Thread(target=ws.run_forever)
    ws_thread.start()

   
    ws_thread.join()

# Call the service to make PuppyPi sit
call_puppy_service()
