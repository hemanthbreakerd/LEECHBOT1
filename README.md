<p align="center">
  <img src="https://raw.githubusercontent.com/alonekingstar77/mirror-leech-telegram-bot/master/web/templates/static/favicon.ico" alt="Logo" width="128" height="128">
</p>

<h1 align="center">⚡ 𝗛𝗘𝗠𝗔𝗡𝗧𝗛 𝗨𝗟𝗧𝗥𝗔 𝗦𝗣𝗘𝗘𝗗 𝗕𝗢𝗧 ⚡</h1>

<p align="center">
  <a href="https://github.com/alonekingstar77/mirror-leech-telegram-bot/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/alonekingstar77/mirror-leech-telegram-bot?style=for-the-badge&color=blue" alt="Contributors">
  </a>
  <a href="https://github.com/alonekingstar77/mirror-leech-telegram-bot/stargazers">
    <img src="https://img.shields.io/github/stars/alonekingstar77/mirror-leech-telegram-bot?style=for-the-badge&color=gold" alt="Stars">
  </a>
  <a href="https://github.com/alonekingstar77/mirror-leech-telegram-bot/network/members">
    <img src="https://img.shields.io/github/forks/alonekingstar77/mirror-leech-telegram-bot?style=for-the-badge&color=green" alt="Forks">
  </a>
  <a href="https://github.com/alonekingstar77/mirror-leech-telegram-bot/LICENSE">
    <img src="https://img.shields.io/github/license/alonekingstar77/mirror-leech-telegram-bot?style=for-the-badge&color=red" alt="License">
  </a>
</p>

<p align="center">
  <b>A High-Performance Telegram Bot for Mirroring, Leeching, and Merging with Ultra-Fast Speeds (Up to 2000 Mbps+).</b>
</p>

---

## 🚀 Overview

This bot is a heavily modified and optimized version of the original Mirror-Leech bot, now managed by **@alonekingstar77**. It is designed for maximum efficiency, stability, and speed. Whether you are mirroring files to Google Drive, leeching to Telegram, or merging multiple video files, this bot handles it all with ease.

- **Developer:** [⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡](https://t.me/alonekingstar77)
- **Support Group:** [Join Here](https://t.me/alonekingstar77)
- **Official Channel:** [Join Here](https://t.me/alonekingstar77)

---

## 🌟 Key Features

### 🛠️ Advanced Functionality
- **Merge Feature:** Easily merge multiple files into one using the new `/merge` command.
- **Ultra-High Speed:** Optimized configurations for downloading and uploading at speeds up to 2000 Mbps.
- **Multi-Cloud Support:** Mirror to Google Drive, Rclone-supported clouds, or Leech to Telegram.
- **QBittorrent & Aria2c:** Fully optimized for torrenting with file selection and seeding capabilities.
- **Sabnzbd Support:** Integrated Usenet downloading with a web interface.
- **JDownloader Integration:** Control your JDownloader tasks directly via the bot.
- **Yt-dlp Support:** Download from thousands of video sites with custom quality selection.

### 🛡️ User & Bot Management
- **Interactive Settings:** Manage bot and user settings via a clean, button-based interface (`/bsetting`, `/usetting`).
- **Force Start & Queueing:** Manage your task priority with a robust queueing system.
- **Search Tools:** Integrated Torrent and Google Drive search.
- **Thumbnail Support:** Custom thumbnails for all your Telegram uploads.

---

## 🛠️ VPS Deployment Guide (Step-by-Step)

Follow these steps to deploy your own instance of the **⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛 𝗨𝗟𝗧𝗥𝗔 𝗦𝗣𝗘𝗘𝗗 𝗕𝗢𝗧⚡** on a VPS.

### 1. Update and Prepare Your System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git docker.io docker-compose -y
```

### 2. Clone the Repository
```bash
git clone https://github.com/alonekingstar77/mirror-leech-telegram-bot mirrorbot/ && cd mirrorbot
```

### 3. Install Required CLI Dependencies
```bash
pip3 install -r requirements-cli.txt
```

### 4. Configure the Bot
- Copy the sample config file:
  ```bash
  cp config_sample.py config.py
  ```
- Edit `config.py` using `nano config.py` and fill in the required variables:
  - `BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
  - `OWNER_ID`: Your Telegram User ID
  - `TELEGRAM_API` & `TELEGRAM_HASH`: Get from [my.telegram.org](https://my.telegram.org)
  - `DATABASE_URL`: Your MongoDB connection string

### 5. Build and Deploy using Docker (Recommended)
```bash
sudo docker compose up --build -d
```
The `-d` flag runs the bot in the background.

### 6. Verify Logs
```bash
sudo docker compose logs --follow
```

---

## 📖 Bot Commands

| Command | Description |
| :--- | :--- |
| `/mirror` | Mirror a link/file to cloud |
| `/leech` | Leech a link/file to Telegram |
| `/merge` | Merge multiple files together (Premium) |
| `/qbmirror` | Mirror torrent via qBittorrent |
| `/ytdl` | Download video via yt-dlp |
| `/status` | Check current task progress |
| `/cancel` | Cancel an ongoing task |
| `/bsetting` | Open Bot Settings (Sudo only) |
| `/usetting` | Open User Settings |

---

## 🤝 Contributing & Support

If you encounter any issues or have feature requests, please join our [Support Group](https://t.me/alonekingstar77). Contributions are always welcome!

---

## ☕ Support the Project

If you find this project useful, consider supporting the developer:
- **Telegram:** [@alonekingstar77](https://t.me/alonekingstar77)
- **Coffee:** [Buy Me A Coffee](https://ko-fi.com/alonekingstar77)

---

<p align="center">
  <b>Built with ❤️ by ⚡𝗛𝗘𝗠𝗔𝗡𝗧𝗛⚡</b>
</p>
