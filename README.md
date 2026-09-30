# FlyEnv Helper — Local Privilege Escalation PoC

Proof of concept for a **local privilege escalation** in FlyEnv's privileged
helper daemon.

> ⚠️ **Authorized security research only.** Run this only on systems you own or
> are explicitly authorized to test.

## Summary

FlyEnv installs a helper daemon that runs as **root** and listens on a Unix
socket (`/tmp/flyenv-helper.sock`). Requests are JSON messages authenticated
with an HMAC‑SHA256 signature using a shared key.

The signing key (`/usr/local/share/FlyEnv/flyenv-helper.key`) is readable by
unprivileged local users. Because any local user can read the key, they can
forge a valid signature for a `tools.runScript` request and have the root helper
execute an arbitrary script — a straightforward **local user → root** escalation.

## Impact

Any local, unprivileged user can execute arbitrary commands as **root**.

## Root cause

- Secret used for authentication is stored with permissions that allow non‑root
  read access, defeating the HMAC gate.
- The `runScript` function executes an attacker‑controlled path as root.

## PoC

`flyenv_lpe_poc.py`:

1. Writes a payload script to `~/.config/FlyEnv/start-poc.sh` (a reverse shell to
   `127.0.0.1:4444` by default).
2. Reads the world‑readable helper key and builds a valid HMAC‑signed
   `tools.runScript` request pointing at the payload.
3. Sends it to the helper socket, which runs the payload as root.

### Usage (demo)

```bash
# Terminal 1 — listener
nc -lvnp 4444

# Terminal 2 — run the PoC
python3 flyenv_lpe_poc.py
```

The listener receives a shell running as `root`.

## Remediation

- Store the helper key with `root`‑only permissions (`0600`, owned by root).
- Authenticate the calling client (verified `clientExe`/pid) rather than relying
  only on a readable shared secret.
- Avoid executing caller‑supplied script paths as root.
