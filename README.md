# Minesweeper Bot

[![Telegram](https://img.shields.io/badge/Telegram-@minesweeper_game_tgbot-black)](https://t.me/minesweeper_game_tgbot)

**🚧 Warning: This bot is in an early release stage. Expect bugs and incomplete features. 🚧**

A Telegram bot that allows users to play Minesweeper directly in their chat.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [License](#license)

## Introduction

The Minesweeper Bot is a fun and interactive Telegram bot that brings the classic Minesweeper game to the chat platform. With this bot, users can enjoy the thrill of uncovering mines and strategically marking safe squares without leaving their Telegram app.

## Installation

Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/dmaksky/minesweeper_tg_bot.git
```

Create user for running bot:

```bash
useradd -d /opt/minesweeper_tg_bot -s /bin/bash minesweeper_bot
```

Copy systemd service to system directory:

```bash
cp /opt/minesweeper_tg_bot/minesweeper_bot.service /etc/systemd/system
systemctl daemon-reload
```

Change permissions in user directory:

```bash
chown -R minesweeper_bot: /opt/minesweeper_tg_bot/
chmod 0700 /opt/minesweeper_tg_bot/
```

Install dependencies to virtual env:

```bash
su - minesweeper_bot
python3.11 -m venv venv
pip install -r requirements.txt
```

Run bot:
```bash
systemctl enable --now minesweeper_bot
```

## Features

- Play Minesweeper directly in Telegram chat.
- Save statistics using sqlite3 database.
- **Game Session Storage Options**: Choose between in-memory storage or Redis for game session persistence.
- **Optional GIF Display**: Enhance the user experience with optional GIFs for displaying win or loss scenarios.
 
## License

This project is licensed under the terms of the [MIT License](LICENSE).
