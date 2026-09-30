# FlyEnv Helper - Local Privilege Escalation PoC Linux

Proof of concept for a **local privilege escalation** in FlyEnv's privileged
helper daemon.

## Impact

Any local, unprivileged user can execute arbitrary commands as **root**.

### Usage

Execute Flyenv and make sure that flyenv-helper is installed and running: 
systemctl status flyenv-helper

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
