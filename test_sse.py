import urllib.request
import json
import threading
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://system-labs-default-rtdb.firebaseio.com/workspaces/test_ws_123.json'

def listen():
    req = urllib.request.Request(url, headers={'Accept': 'text/event-stream'})
    response = urllib.request.urlopen(req, context=ctx)
    print("Connected to SSE")
    for line in response:
        print(line.decode('utf-8').strip())

t = threading.Thread(target=listen)
t.daemon = True
t.start()

time.sleep(2)

print("Sending PUT...")
data = json.dumps({"data": json.dumps({"a": 1, "b": 2, "tasks": [{"id": 1, "done": True}]})}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='PUT')
req.add_header('Content-Type', 'application/json')
res = urllib.request.urlopen(req, context=ctx)
print("PUT Status:", res.status)

time.sleep(3)
