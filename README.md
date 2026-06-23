<p align="center">
  <img src="https://abrehamrahi.ir/o/public/rNf0ej8l/" alt="aiodot logo" width="200">
</p>

<h1 align="center">aiodot 🚀</h1>
<p align="center">
  <b>Async Python client for MyDot.one social platform</b><br>
  Build bots, automation, and tools with ease.
</p>

<p align="center">
  <a href="https://pypi.org/project/aiodot/">
    <img src="https://badge.fury.io/py/aiodot.svg" alt="PyPI version">
  </a>
  <a href="https://pypi.org/project/aiodot/">
    <img src="https://img.shields.io/pypi/pyversions/aiodot.svg" alt="Python">
  </a>
  <a href="https://github.com/karbaladevir/aiodot/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
</p>

---

**`aiodot`** is an asynchronous Python library for [MyDot.one](https://mydot.one). Built with `aiohttp` — fast, async-first, session-based like aiogram.

---

## ✨ Features

- ⚡ **Async-first** — Built on aiohttp
- 🔑 **Login with password** — No token needed
- 💾 **Session persistence** — Login once, auto-loads next time
- 🔄 **Auto token refresh** — Handles 401 gracefully
- 📦 **60+ endpoints** — Full API coverage
- 🖼️ **Avatar upload** — Built-in support
- 💰 **Wallet management** — Full wallet API
- 🧵 **Thread management** — Composer and thread support
- 🎯 **Type hints** — Full type annotations

---

## 📦 Installation

```bash
pip install aiodot
```

---

## 💡 Quick Start

### Login with password:

```python
import asyncio
from aiodot import MyDotClient

async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login("username", "password")

        me = await client.get_me()
        print(f"@{me.username}")

        dot = await client.create_dot("Hello aiodot! 🚀")
        print(dot.url)

asyncio.run(main())
```

### Or login with token:

```python
async with MyDotClient(token="your-token", session_file="session.json") as client:
    me = await client.get_me()
```

---

## 🤖 Echo Bot

```python
import asyncio
from aiodot import MyDotClient

async def main():
    processed = set()
    async with MyDotClient(session_file="session.json") as c:
        await c.login("username", "password")
        print(f"🤖 @{(await c.get_me()).username} started!")

        while True:
            for n in (await c.get_notifications(10)).get("results", []):
                if n.get("id") in processed:
                    continue
                processed.add(n.get("id"))
                if n.get("type") == "mention":
                    d = n.get("dot", {})
                    if d.get("id"):
                        await c.reply(d["id"], "Hello! 🤖")
            await asyncio.sleep(15)

asyncio.run(main())
```

---

## 📖 Complete API Reference

| Category | Methods |
|----------|---------|
| **Auth** | `login()`, `login_with_token()` |
| **Profile** | `get_me()`, `update_profile()`, `upload_avatar()`, `upload_avatar_request()`, `upload_avatar_put()`, `get_profile_visibility()`, `set_profile_visibility()` |
| **Dots** | `create_dot()`, `get_dot()`, `reply()`, `repost()`, `quote()`, `like()`, `unlike()`, `bookmark()`, `unbookmark()`, `edit_dot()`, `delete_dot()`, `get_replies()`, `get_reposts()`, `get_quotes()`, `get_dot_likes()`, `undo_repost()`, `set_reply_permission()` |
| **Social** | `follow()`, `unfollow()`, `block()`, `unblock()`, `mute()`, `unmute()` |
| **Users** | `search_users()`, `get_user_followers()`, `get_user_following()`, `get_user_dots()`, `get_user_replies()`, `get_user_likes()` |
| **Feed** | `home_feed()`, `following_feed()`, `explore_users_suggestions()`, `get_topic_dots()` |
| **Notifications** | `get_notifications()`, `mark_all_read()`, `get_notification_preferences()`, `update_notification_preferences()` |
| **Trending** | `get_trending_hashtags()`, `get_trending_media()` |
| **Bookmarks** | `get_bookmarks()` |
| **Wallet** | `client.wallet.create()`, `client.wallet.list()`, `client.wallet.get()`, `client.wallet.transactions()`, `client.wallet.toggle_default()` |
| **Threads** | `get_threads()`, `create_threads()`, `get_threads_view()`, `add_thread()`, `remove_thread()` |
| **Composer** | `get_composer_state()`, `reset_composer()` |
| **Media** | `upload_media()` |
| **Other** | `get_alerts()`, `get_invites()`, `get_wallets()`, `get_2fa_state()`, `get_star_settings()`, `get_star_transactions()` |

---

## 📈 What's New

### v1.2.0
- 🔑 **Password login** — `client.login(username, password)`
- 🖼️ **Avatar upload** — Full upload flow (`upload_avatar`, `upload_avatar_request`, `upload_avatar_put`)
- 💰 **Wallet management** — `client.wallet.*` (create, list, get, transactions, toggle default)
- 🧵 **Thread management** — Composer and thread endpoints
- 👤 **Extended User model** — 25+ fields including badges, KYC, join date, visibility
- 📦 **New models** — `Thread`, `ReplyPermission`
- 🔗 **Extended profile update** — `selected_badge_id`, `avatar_key`, `birthdate`
- 📝 **Improved auth** — Cleaner code, session persistence

### v1.0.0
- ⚡ Initial release
- 50+ endpoints (dots, feed, notifications, trending, social, search)
- Session persistence (like aiogram)
- Auto token refresh
- Type hints & dataclasses

---

## ⚠️ Disclaimer

Unofficial library. Use responsibly per MyDot.one Terms of Service.

---

## 📡 Community

- 📢 **Telegram:** [@aiodotlib](https://t.me/aiodotlib)
- 💬 **Bale:** [ble.ir/aiodot](https://ble.ir/aiodot)
- 📖 **Documentation:** [aiodot docs](https://samon-fs.github.io/aiodot-docsweb/)
- 🌐 **Website:** [karbaladev.ir](https://karbaladev.ir)

---

## 📄 License

MIT © [karbaladev.ir](https://karbaladev.ir) — [View License](https://github.com/karbaladevir/aiodot/blob/main/LICENSE)