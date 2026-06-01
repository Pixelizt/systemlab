const https = require('https');
const RTDB_URL = 'https://system-labs-default-rtdb.firebaseio.com';
const path = 'workspaces/test_ws_123.json';

const req = https.request(`${RTDB_URL}/${path}`, {
  headers: { 'Accept': 'text/event-stream' }
}, (res) => {
  res.on('data', (chunk) => {
    console.log('--- EVENT SOURCE DATA ---');
    console.log(chunk.toString());
  });
});
req.end();

setTimeout(() => {
  console.log('Sending PUT request...');
  const data = JSON.stringify({ data: JSON.stringify({ a: 1, b: 2, tasks: [{ id: 1, done: true }] }) });
  const putReq = https.request(`${RTDB_URL}/${path}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' }
  }, (putRes) => {
    console.log('PUT response status:', putRes.statusCode);
  });
  putReq.write(data);
  putReq.end();
}, 2000);

setTimeout(() => process.exit(0), 5000);
