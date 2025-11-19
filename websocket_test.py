#!/usr/bin/env python3
import websocket
import ssl
import json

def on_message(ws, message):
    print(f"Received: {message}")
    # Check for flag
    if 'flag' in message.lower() or 'FLAG' in message:
        import re
        flags = re.findall(r'[Ff][Ll][Aa][Gg]\{.*?\}|Nutanix\{.*?\}', message)
        if flags:
            print(f"\n*** FLAG FOUND: {flags} ***")
    ws.close()

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("WebSocket connection opened")
    # Send a test message
    ws.send("hello")
    ws.send("flag")
    ws.send("get_flag")

if __name__ == "__main__":
    # Try WebSocket connection
    url = "wss://nusock1-2447.ctf.nutanix.com/"
    print(f"Connecting to {url}...")
    
    ws = websocket.WebSocketApp(url,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close,
                              on_open=on_open)
    
    # Try with SSL
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
