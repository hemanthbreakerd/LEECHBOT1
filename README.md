# 🚀 Ultimate Ultra High Speed Mirror-Leech Bot

A professional, extremely optimized, and feature-rich Telegram Bot for Mirroring and Leeching files at Light Ultra High Speed. Powered by TDLib (Pytdbot), Aria2c, qBittorrent, and FFmpeg.

---

## 🔥 Key Features

- **⚡ Light Ultra High Speed (Target 10,000mbps+):**
  - **Downloads:** Multiple chunk parallel downloading with up to 1024 workers for Premium users.
  - **Uploads:** Concurrent multi-file uploading (up to 50 files simultaneously).
  - **Core:** Highly optimized TDLib configuration with 500 workers and 1000 network threads.
  - **Aria2c:** Turbocharged with 128 connections and 128 splits per server.

- **🔄 Intelligent Sequential Merge:**
  - Automatically joins split files (`.001`, `.002`, etc.) sequentially.
  - **No Disk Stocking:** Deletes processed parts immediately after appending to save disk space.
  - Fully integrated into the task flow: Download ➜ Extract ➜ Join ➜ Metadata ➜ Upload.

- **📂 Advanced File Management:**
  - **Extraction:** Support for all major formats (Zip, 7z, Rar, ISO, etc.) with password support.
  - **Compression:** Zip your files with optional passwords.
  - **Metadata:** Add custom metadata to media files using FFmpeg.
  - **Splitting:** Automatically split large files to bypass Telegram limits (up to 4GB for Premium).

---

## 🛠️ Deployment Guides (100% Success)

### 🖥️ VPS Deployment (via Termius or SSH)

1. **Install Prerequisites:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3-pip python3-venv git ffmpeg aria2 qbittorrent-nox 7zip
   ```

2. **Clone and Setup:**
   ```bash
   git clone https://github.com/your-repo/mirror-leech-bot.git mltb && cd mltb
   ```

3. **Install Requirements:**
   ```bash
   python3 -m pip install --upgrade pip
   pip3 install -r requirements.txt
   ```

4. **Configure:**
   - Create a `config.env` file. Fill in: `BOT_TOKEN`, `TELEGRAM_API`, `TELEGRAM_HASH`, `OWNER_ID`, `DATABASE_URL`.

5. **Run:**
   ```bash
   bash aria-nox-nzb.sh && python3 -m bot
   ```

### 📱 Termux Deployment (Android)

1. **Setup Termux:**
   ```bash
   pkg update && pkg upgrade -y
   pkg install -y python git ffmpeg aria2 qbittorrent 7zip-full
   ```

2. **Clone and Install:**
   ```bash
   git clone https://github.com/your-repo/mirror-leech-bot.git mltb && cd mltb
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run:**
   ```bash
   bash aria-nox-nzb.sh && python3 -m bot
   ```

### 🐳 Docker Deployment

1. **Build and Run:**
   ```bash
   docker build -t mltb .
   docker run -d --name mltb --env-file config.env mltb
   ```

---

## ⚙️ Configuration Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `BOT_TOKEN` | Your Telegram Bot Token | Mandatory |
| `TELEGRAM_API` | Your API ID from my.telegram.org | Mandatory |
| `TELEGRAM_HASH` | Your API HASH from my.telegram.org | Mandatory |
| `JOIN` | Enable global sequential merging | `False` |
| `LEECH_SPLIT_SIZE` | Size to split leech files | `2097152000` |

---

## 🛡️ Troubleshooting

- **ERROR: requirements.txt not found:** Ensure you are in the `/mltb` directory before running `pip install`.
- **Git Error in Update:** We have added `safe.directory $(pwd)` to `update.py` to fix common permission issues on VPS.
- **Speed Issues:** Use a VPS with at least 1Gbps network and a Premium Telegram account for maximum 10,000mbps+ target throughput.

---

**Note:** Always use this bot responsibly and respect Telegram's Terms of Service.
