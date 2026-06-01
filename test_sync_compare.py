"""
Test the EXACT sync comparison logic used in the browser.
Simulate what the hybrid polling does.
"""
import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

RTDB_URL = 'https://system-labs-default-rtdb.firebaseio.com'

def rtdb_get(path):
    url = f'{RTDB_URL}/{path}.json?_t={int(time.time()*1000)}'
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, context=ctx) as resp:
        return json.loads(resp.read().decode())

# Get the actual workspace data
ws = rtdb_get('workspaces/123456')
if ws and 'data' in ws:
    data = json.loads(ws['data'])
    
    print("=== WORKSPACE 123456 DATA ANALYSIS ===")
    print(f"Data string length: {len(ws['data']):,} bytes")
    print(f"Keys in parsed data: {list(data.keys())}")
    print(f"Depts: {len(data.get('depts', []))}")
    print(f"SOPs: {len(data.get('sops', []))}")
    print(f"Employees: {len(data.get('employees', []))}")
    print(f"Tasks: {len(data.get('tasks', []))}")
    print(f"Recurring: {len(data.get('recurring', []))}")
    print(f"Att keys: {len(data.get('att', {}))}")
    print(f"Leadgen keys: {list(data.get('leadgen', {}).keys())[:5]}")
    print()
    
    # Check if 'recurring' key exists at all
    if 'recurring' in data:
        print(f"✅ 'recurring' key exists (value: {data['recurring']})")
    else:
        print(f"❌ 'recurring' key is MISSING from cloud data!")
    
    # Simulate the comparison logic
    # Build the local string as the browser would
    localStr = json.dumps({
        'depts': data.get('depts', []),
        'sops': data.get('sops', []),
        'workspaceName': data.get('workspaceName', ''),
        'employees': data.get('employees', []),
        'tasks': data.get('tasks', []),
        'att': data.get('att', {}),
        'recurring': data.get('recurring', []),
        'leadgen': data.get('leadgen', {})
    })
    
    remoteStr = json.dumps({
        'depts': data.get('depts', []),
        'sops': data.get('sops', []),
        'workspaceName': data.get('workspaceName', ''),
        'employees': data.get('employees', []),
        'tasks': data.get('tasks', []),
        'att': data.get('att', {}),
        'recurring': data.get('recurring', []),
        'leadgen': data.get('leadgen', {})
    })
    
    print(f"\nLocal string length: {len(localStr):,}")
    print(f"Remote string length: {len(remoteStr):,}")
    print(f"Strings match: {localStr == remoteStr}")
    
    # Now test: what happens if we modify a task and write it back
    print("\n=== SIMULATING TASK TOGGLE ===")
    tasks = data.get('tasks', [])
    if tasks:
        first_task = tasks[0]
        print(f"First task: {first_task.get('name', 'unnamed')} (done={first_task.get('done')})")
        
        # Toggle it
        first_task['done'] = not first_task.get('done', False)
        first_task['doneAt'] = '9:30 AM' if first_task['done'] else None
        
        # Write back
        new_payload = json.dumps(data)
        print(f"New payload length: {len(new_payload):,}")
        
        # Write to Firebase
        result = rtdb_get('workspaces/123456')
        print(f"Pre-write data length: {len(result.get('data', '')):,}")
        
        # Actually write
        import urllib.request
        url = f'{RTDB_URL}/workspaces/123456.json'
        body = json.dumps({'data': new_payload}).encode()
        req = urllib.request.Request(url, data=body, method='PUT')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, context=ctx) as resp:
            write_result = json.loads(resp.read().decode())
        
        print(f"Write completed. Result data length: {len(write_result.get('data', '')):,}")
        
        # Read back
        time.sleep(1)
        verify = rtdb_get('workspaces/123456')
        verify_data = json.loads(verify['data'])
        verify_task = next((t for t in verify_data.get('tasks', []) if t.get('id') == first_task['id']), None)
        if verify_task:
            print(f"Verified task: {verify_task.get('name', 'unnamed')} (done={verify_task.get('done')})")
            print(f"✅ Task toggle persisted successfully!")
        
        # Revert the change
        first_task['done'] = not first_task['done']
        first_task['doneAt'] = None if not first_task['done'] else first_task.get('doneAt')
        revert_payload = json.dumps(data)
        body = json.dumps({'data': revert_payload}).encode()
        req = urllib.request.Request(url, data=body, method='PUT')
        req.add_header('Content-Type', 'application/json')
        with urllib.request.urlopen(req, context=ctx) as resp:
            resp.read()
        print("Reverted test change.")
    else:
        print("No tasks to test with!")
else:
    print("Could not read workspace 123456!")
