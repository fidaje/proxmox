# 🤖 Proxmox Telegram Bot

A Python-based Telegram bot for monitoring and managing a Proxmox VE server directly from Telegram chat.

The project allows you to:

- monitor VM and LXC container status;
- check CPU, RAM, and storage usage;
- start or stop virtual machines and containers;
- shut down the Proxmox node;
- restrict access to authorized Telegram users only.

The bot uses:

- `python-telegram-bot` (Asynchronous)
- `proxmoxer`
- environment variables via `.env`
- optional Docker deployment
- GitHub Actions for automated CI/CD

---

# 📦 Features

## 🔍 Resource Monitoring
Available commands to retrieve Proxmox node information:
- CPU usage
- RAM usage
- HDD usage
- SSD/ZFS usage
- overall storage statistics

## 🖥️ VM & Container Management
The bot can:
- list all virtual machines
- list all LXC containers
- display current status (`running` / `stopped`)
- start a VM/container
- stop a VM/container

## ⚡ Asynchronous & Robust
- **Non-blocking Architecture:** utilizes `asyncio` to ensure the bot remains responsive to other users/commands even while waiting for Proxmox API responses.
- **Error Handling:** gracefully handles API timeouts or Proxmox offline states by alerting the user on Telegram, instead of crashing.

## 🔒 Security
Access is restricted to Telegram users defined in the environment variables:
```env
AUTHORIZED_USER_ID
AUTHORIZED_USER_ID_2
AUTHORIZED_USER_ID_3
...

Only authorized users can execute commands.

You can also protect a specific container (for example the one running the bot itself):

```env
TELEGRAM_CT=100

```

This prevents accidental shutdown of the bot container.

## ⚡ Node Shutdown

A dedicated command is available to power off the Proxmox node.
⚠️ Use carefully.

---

# 🏗️ Project Structure

```text
.
├── main.py           # Telegram bot entry point & Async Handlers
├── proxmox.py        # Proxmox API integration logic
├── utils.py          # Unified Utility/helper functions
├── requirements.txt  # Clean, minimal dependencies
├── Dockerfile        # Secure, cached Docker build
└── README.md

```

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/fidaje/proxmox.git
cd proxmox

```

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate

```

## 3. Install dependencies

```bash
pip install -r requirements.txt

```

---

# ⚙️ Configuration

Create a `.env` file in the project root.

## Example `.env`

```env
# =========================
# Telegram
# =========================
TELEGRAM_TOKEN=your_bot_token
AUTHORIZED_USER_ID=123456789
AUTHORIZED_USER_ID_2=987654321

# Protected container
TELEGRAM_CT=100

# =========================
# Proxmox API
# =========================
PROXMOX_HOST=proxmox_ip_or_hostname
PROXMOX_USER=api-user@pam
PROXMOX_TOKEN=token-value
NAME_PROXMOX=token-name
NODE=pve

# =========================
# Privileged token
# =========================
SYS=system-token-value
SYS_USER=root@pam
NAME_SYS=system-token-name

```

---

# 🔑 Proxmox API Permissions

It is recommended to create:

* one standard token for monitoring operations;
* one privileged token for administrative operations.

Suggested permissions:

* `VM.Audit`
* `VM.PowerMgmt`
* `Datastore.Audit`
* `Sys.Audit`
* `Sys.PowerMgmt`

---

# ▶️ Running the Project

## Local execution

```bash
python main.py

```

The bot will start listening for Telegram messages using polling.

---

# 🐳 Docker

The provided Dockerfile is optimized for **fast builds** (using layer caching) and **security** (running as a restricted non-root user).

## Build the image

```bash
docker build -t proxmox-telegram-bot .

```

## Run the container

```bash
docker run -d \
  --name proxmox-bot \
  --env-file .env \
  proxmox-telegram-bot

```

---

# 💬 Telegram Commands

| Command | Description |
| --- | --- |
| `/list` | List VMs and containers |
| `/containers` | Show all containers |
| `/vms` | Show all virtual machines |
| `/info` | Display system information |
| `/change <vmid>` | Start or stop a VM/container |
| `/shutdown` | Shut down the Proxmox node |
| `/help` | Display help message |

---

# 📊 Example Output

## `/list`

```text
Containers and virtual machines status on pve:

📦 100: docker 🟢
📦 101: nginx 🔴

🖥️ 200: Ubuntu Server 🟢
🖥️ 201: Windows VM 🔴

```

## `/info`

```text
CPU usage on pve:
🧠: 12.4%

RAM usage on pve:
🕊️: 42.1% (13.4 GB / 32 GB)

SSD usage on pve:
💾: 58.7% (120 GB / 256 GB)

```

---

# ⚠️ Current Limitations

The project currently:

* uses Telegram polling instead of webhooks;
* supports a single Proxmox node;

---

# 💡 Possible Improvements

* multi-node support;
* full Proxmox cluster support;
* automatic notifications;
* web dashboard;
* RBAC authentication;
* persistent logging;
* Prometheus/Grafana metrics;
* Docker Compose deployment;
* Telegram webhook support.

---


# 👨‍💻 Author

Personal project for managing a Proxmox infrastructure through Telegram.
