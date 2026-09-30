# FlyEnv Helper - Local Privilege Escalation PoC Linux

Proof of concept for a **local privilege escalation** in FlyEnv's privileged
helper daemon.

## Impact

Any local, unprivileged user can execute arbitrary commands as **root**.

### Usage

Execute Flyenv and make sure that flyenv-helper is installed and running: 

```bash
# Terminal 1
systemctl status flyenv-helper

nc -lvnp 4444

# Terminal 2 - run the PoC
python3 flyenv_lpe_poc.py
```
