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

- **🛠️ User-Centric Controls:**
  - **Join Toggle:** Enable/Disable merging via `/us` (User Settings) inline menu.
  - **Direct DM:** Leeched files are sent directly to your Bot DM by default.
  - **Custom Destination:** Set any chat/channel as your upload destination.

---

## 🛠️ VPS Deployment Guide (Step-by-Step)

### Option 1: Docker Deployment (Recommended)

1. **Install Docker:**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/mirror-leech-bot.git && cd mirror-leech-bot
   ```

3. **Configure Environment:**
   - Create a `config.env` file in the root directory.
   - Fill in mandatory vars: `BOT_TOKEN`, `TELEGRAM_API`, `TELEGRAM_HASH`, `OWNER_ID`, `DATABASE_URL`.

4. **Build and Run:**
   ```bash
   docker build -t mltb .
   docker run -d --name mltb --env-file config.env mltb
   ```

### Option 2: Manual Deployment

1. **Install Dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip ffmpeg aria2 qbittorrent-nox 7zip
   ```

2. **Clone and Install Python Packages:**
   ```bash
   git clone https://github.com/your-repo/mirror-leech-bot.git && cd mirror-leech-bot
   pip3 install -r requirements.txt
   ```

3. **Setup Configuration:**
   - Rename `config.sample.env` to `config.env` and edit it.

4. **Start the Bot:**
   ```bash
   bash aria-nox-nzb.sh && python3 -m bot
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
| `USER_TRANSMISSION` | Use User Session for high-speed leeching | `False` |

---

## 🛡️ License & Credits

This project is licensed under the MIT License. Special thanks to the developers of Pytdbot, Aria2, and qBittorrent.

**Note:** Always use this bot responsibly and respect Telegram's Terms of Service.
