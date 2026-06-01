import urllib.request
import json
import threading
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://system-labs-default-rtdb.firebaseio.com/workspaces/test_ws_123.json?sse=123456789'

def listen():
    try:
        req = urllib.request.Request(url, headers={'Accept': 'text/event-stream'})
        response = urllib.request.urlopen(req, context=ctx)
        print("Connected to SSE with query param")
        for line in response:
            print(line.decode('utf-8').strip())
    except Exception as e:
        print("SSE connection failed:", e)

t = threading.Thread(target=listen)
t.daemon = True
t.start()

time.sleep(3)
