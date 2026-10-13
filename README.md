# FlyEnv - Local Privilege Escalation PoC Linux

Proof of concept for a **local privilege escalation** in FlyEnv.

## Impact

Any local, unprivileged user can execute arbitrary commands as **root**. Affected versions FlyEnv ≤ 4.19.1.

### Usage

Execute Flyenv and make sure that flyenv-helper is installed and running: 

```bash
# Terminal 1
systemctl status flyenv-helper

nc -lvnp 4444

# Terminal 2 - run the PoC
python3 flyenv_lpe_poc.py
```

<img width="1181" height="707" alt="POC2" src="https://github.com/user-attachments/assets/eb31cd03-0c52-4ca4-8c10-ee111af6b1bf" />
