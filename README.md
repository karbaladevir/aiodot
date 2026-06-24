<p align="center">
  <a href="./README.md">🇺🇸 English</a> |
  <a href="./README.fa.md">🇮🇷 فارسی</a>
</p>

<p align="center">
  <img src="https://abrehamrahi.ir/o/public/rNf0ej8l/" alt="aiodot logo" width="200">
</p>

<h1 align="center">aiodot 🚀</h1>

<p align="center">
  <b>Async Python client for MyDot</b><br>
  Build bots, self-clients, automation tools and integrations with ease.
</p>

---

## About

**aiodot** is an asynchronous Python library for **MyDot**, a microblogging social platform similar to X (formerly Twitter).

The library is built on top of **aiohttp** and provides a clean, modern, async-first API for interacting with MyDot. Whether you're building bots, automation tools, analytics systems, or personal self-clients, aiodot makes it simple.

---

## Features

* ⚡ Fully asynchronous architecture
* 🔑 Login using username and password
* 💾 Persistent sessions
* 🔄 Automatic token refresh
* 📦 60+ supported endpoints
* 🖼️ Avatar upload support
* 💰 Wallet API support
* 🧵 Thread management
* 🤖 Ideal for bots and self-clients
* 🎯 Full type hints

---

## Installation

```bash
pip install aiodot
```

---

## Quick Start

```python
import asyncio
from aiodot import MyDotClient

async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login("username", "password")

        me = await client.get_me()
        print(f"@{me.username}")

        dot = await client.create_dot("Hello MyDot! 🚀")
        print(dot.url)

asyncio.run(main())
```

---

## Why aiodot?

* Easy to use
* Async-first design
* Session management built-in
* Covers most public MyDot APIs
* Designed for automation and tooling

---

## Use Cases

* 🤖 MyDot bots
* 👤 Self-clients
* 📊 Analytics tools
* 📰 Scheduled posting
* 🔔 Notification monitoring
* 🧪 Experiments and integrations

---

## Community

* Telegram: @aiodotlib
* Bale: ble.ir/aiodot
* Documentation: aiodot Docs
* Website: karbaladev.ir

---

## Disclaimer

This is an unofficial library and is not affiliated with the MyDot team.

Use responsibly and in accordance with MyDot's Terms of Service.

---

## License

MIT License
