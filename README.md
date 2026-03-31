# Advanced Mirror-Leech Telegram Bot

An extremely powerful and highly optimized Telegram Bot based on [python-aria-mirror-bot](https://github.com/lzzy12/python-aria-mirror-bot). This bot is designed for high-performance mirroring and leeching from various sources to multiple destinations like Google Drive, Telegram, or Rclone-supported clouds.

---

## 🚀 Key Performance Features

- **Extreme Download Speed**: Telegram files are downloaded using a multi-chunk parallel processing engine (up to 128 concurrent connections), maximizing server bandwidth.
- **Ultra-Fast Uploads**: Concurrent multi-file uploading allows the bot to process up to 10 files simultaneously within a single task, reaching speeds of up to 2000mbps on optimized networks.
- **Sequential Join (Non-Stocking)**: Automatically merge split files part-by-part. This method saves significant disk space by deleting source parts immediately after they are appended to the main file.
- **Optimized TDLib**: Customized TDLib worker pools and network thread configurations for maximum throughput and reliability.

---

## 🛠 Features Overview

### Transfer & Storage
- **Google Drive**: Download/Upload/Clone with Service Account support and Duplicate check.
- **Rclone**: Transfer to any Rclone-supported cloud with custom flags and remote selection.
- **Telegram Leech**: Upload files to Telegram as Documents or Media with custom thumbnails and split support.
- **Direct Links**: Support for premium direct link generators and various file hosts.

### Task Management
- **Sequential Join**: Configurable global/user setting to merge split parts automatically.
- **Extraction & Compression**: Powerful 7z integration for zip/unzip with password support.
- **Metadata Management**: Apply custom metadata to files before upload.
- **Queue System**: Smart queueing for parallel downloads and uploads.

### User Control
- **Interactive Settings**: Manage your preferences via the `/us` (User Settings) menu.
- **Search Integration**: Search for torrents directly via the bot using multiple plugins.
- **RSS Feeds**: Automated tracking and downloading from RSS feeds.

---

## 🖥 VPS Deployment Guide (Step-by-Step)

This guide provides two methods for deploying the bot on your VPS.

### Method 1: Using Docker (Recommended)

1. **Install Docker**:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose
   ```
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/anasty17/mirror-leech-telegram-bot mltb/ && cd mltb
   ```
3. **Configure the Bot**:
   - Copy the sample config: `cp config_sample.py config.py`
   - Edit `config.py` with your `BOT_TOKEN`, `OWNER_ID`, `TELEGRAM_API`, and `TELEGRAM_HASH`.
4. **Build and Start**:
   ```bash
   sudo docker compose up -d --build
   ```

### Method 2: Manual Deployment (Ubuntu/Debian)

1. **Update and Install Dependencies**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install -y python3 python3-pip python3-venv aria2 qbittorrent-nox ffmpeg 7zip
   ```
2. **Clone and Setup Environment**:
   ```bash
   git clone https://github.com/anasty17/mirror-leech-telegram-bot mltb/ && cd mltb
   python3 -m venv mltbenv
   source mltbenv/bin/activate
   pip3 install -r requirements.txt
   ```
3. **Configure**:
   - Edit `config.py` as mentioned in the Docker section.
4. **Prepare Startup Script**:
   - Ensure `start.sh` is executable: `chmod +x start.sh`
5. **Run the Bot**:
   ```bash
   ./start.sh
   ```

---

## ⚙️ Configuration Parameters

| Parameter | Description |
| :--- | :--- |
| `BOT_TOKEN` | Your bot token from @BotFather. |
| `OWNER_ID` | Your Telegram User ID. |
| `TELEGRAM_API` | API ID from my.telegram.org. |
| `TELEGRAM_HASH` | API Hash from my.telegram.org. |
| `JOIN` | Enable/Disable automatic merging of split files (Default: False). |
| `LEECH_SPLIT_SIZE` | Max size for leeched file parts (up to 4GB for premium). |

---

## 🤝 Support & Contributions

Join our community for updates and support:
- **Telegram Channel**: [MLTB Official](https://t.me/mltb_official_channel)
- **Telegram Group**: [MLTB Support](https://t.me/mltb_official_support)

---
*Maintained with ❤️ by our contributors.*
