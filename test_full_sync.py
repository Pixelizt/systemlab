"""
Full end-to-end test of SystemLab real-time sync.
1. Read current state from Firebase
2. Modify a task
3. Write it back
4. Verify SSE event fires
5. Read again and verify the update persisted
"""
import urllib.request
import json
import ssl
import time
import threading

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

RTDB_URL = 'https://system-labs-default-rtdb.firebaseio.com'

def rtdb_get(path):
    url = f'{RTDB_URL}/{path}.json?_t={int(time.time()*1000)}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode())

def rtdb_set(path, data):
    url = f'{RTDB_URL}/{path}.json'
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, method='PUT')
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode())

# --- Step 1: Get list of workspaces ---
print("=" * 60)
print("STEP 1: List all workspace IDs in Firebase")
print("=" * 60)
workspaces = rtdb_get('workspaces')
if workspaces:
    for ws_id in workspaces:
        ws_data = workspaces[ws_id]
        if isinstance(ws_data, dict) and 'data' in ws_data:
            try:
                parsed = json.loads(ws_data['data'])
                name = parsed.get('workspaceName', 'Unknown')
                emp_count = len(parsed.get('employees', []))
                task_count = len(parsed.get('tasks', []))
                recurring_count = len(parsed.get('recurring', []))
                print(f"  Workspace: {ws_id}")
                print(f"    Name: {name}")
                print(f"    Employees: {emp_count}")
                print(f"    Tasks: {task_count}")
                print(f"    Recurring templates: {recurring_count}")
                print()
            except:
                print(f"  Workspace: {ws_id} (unparseable data)")
        else:
            print(f"  Workspace: {ws_id} (no data key)")

# --- Step 2: Test SSE listener ---
print("=" * 60)
print("STEP 2: Test SSE listener on first workspace")
print("=" * 60)

first_ws = list(workspaces.keys())[0] if workspaces else None
if not first_ws:
    print("No workspaces found!")
    exit(1)

print(f"Testing SSE on workspace: {first_ws}")

sse_received = []
def listen_sse():
    url = f'{RTDB_URL}/workspaces/{first_ws}.json?sse={int(time.time()*1000)}'
    req = urllib.request.Request(url, headers={'Accept': 'text/event-stream'})
    try:
        resp = urllib.request.urlopen(req, context=ctx)
        for line in resp:
            decoded = line.decode().strip()
            if decoded.startswith('data:'):
                sse_received.append(decoded)
                print(f"  SSE received: {decoded[:120]}...")
    except Exception as e:
        print(f"  SSE error: {e}")

t = threading.Thread(target=listen_sse, daemon=True)
t.start()
time.sleep(2)

# --- Step 3: Write a test modification ---
print()
print("=" * 60)
print("STEP 3: Write a test modification to trigger SSE")
print("=" * 60)

current = rtdb_get(f'workspaces/{first_ws}')
if current and 'data' in current:
    parsed = json.loads(current['data'])
    # Add a timestamp marker to verify write worked
    parsed['_syncTest'] = f'test_{int(time.time())}'
    
    # Write back
    result = rtdb_set(f'workspaces/{first_ws}', {'data': json.dumps(parsed)})
    print(f"  Write result keys: {list(result.keys()) if isinstance(result, dict) else type(result)}")
    
    # Wait for SSE
    print("  Waiting 3 seconds for SSE event...")
    time.sleep(3)
    
    if len(sse_received) > 1:  # First one is the initial 'put' on connect
        print(f"  ✅ SSE events received: {len(sse_received)}")
    else:
        print(f"  ⚠️  Only {len(sse_received)} SSE events (expected > 1)")
    
    # --- Step 4: Read back and verify ---
    print()
    print("=" * 60)
    print("STEP 4: Read back and verify the update")
    print("=" * 60)
    
    verified = rtdb_get(f'workspaces/{first_ws}')
    if verified and 'data' in verified:
        v_parsed = json.loads(verified['data'])
        if v_parsed.get('_syncTest') == parsed['_syncTest']:
            print(f"  ✅ Verified: _syncTest = {v_parsed['_syncTest']}")
        else:
            print(f"  ❌ MISMATCH: expected {parsed['_syncTest']}, got {v_parsed.get('_syncTest')}")
        
        # Show data size
        data_size = len(verified['data'])
        print(f"  Data size: {data_size:,} bytes")
        print(f"  Recurring count: {len(v_parsed.get('recurring', []))}")
        print(f"  Task count: {len(v_parsed.get('tasks', []))}")
    else:
        print("  ❌ Could not read back data!")
    
    # Clean up test marker
    del parsed['_syncTest']
    rtdb_set(f'workspaces/{first_ws}', {'data': json.dumps(parsed)})
    print("  Cleaned up test marker")
else:
    print("  No data in workspace!")

print()
print("=" * 60)
print("AUDIT COMPLETE")
print("=" * 60)
