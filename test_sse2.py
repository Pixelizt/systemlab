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

print("Sending first PUT...")
data1 = json.dumps({"data": "STRING1"}).encode('utf-8')
req1 = urllib.request.Request(url, data=data1, method='PUT')
req1.add_header('Content-Type', 'application/json')
res1 = urllib.request.urlopen(req1, context=ctx)

time.sleep(2)

print("Sending second PUT (changing only data)...")
data2 = json.dumps({"data": "STRING2"}).encode('utf-8')
req2 = urllib.request.Request(url, data=data2, method='PUT')
req2.add_header('Content-Type', 'application/json')
res2 = urllib.request.urlopen(req2, context=ctx)

time.sleep(3)
