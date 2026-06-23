"""aiodot Echo Bot - replies to mentions automatically."""

import asyncio
from datetime import datetime
from aiodot import MyDotClient

SESSION_FILE = "session.json"
USERNAME = ""
PASSWORD = ""

processed = set()


async def main():
    async with MyDotClient(session_file=SESSION_FILE) as client:
        await client.login(USERNAME, PASSWORD)

        me = await client.get_me()
        print(f"🤖 Bot started: @{me.username}")
        print(f"   Listening for mentions...\n")

        while True:
            try:
                notifs = await client.get_notifications(page_size=10)

                for notif in notifs.get("results", []):
                    nid = notif.get("id")
                    ntype = notif.get("type")

                    if nid in processed:
                        continue
                    processed.add(nid)

                    if ntype != "mention":
                        continue

                    dot = notif.get("dot", {})
                    dot_id = dot.get("id")
                    author = dot.get("author", {})
                    content = dot.get("content", "")
                    username = author.get("username", "user")

                    if not dot_id:
                        continue

                    print(f"📩 @{username}: {content[:60]}...")

                    if "سلام" in content:
                        await client.reply(dot_id, f"سلام @{username}! خوبی؟ 😊")
                        print(f"   👋 Replied: hello")

                    elif "ساعت" in content:
                        now = datetime.now().strftime("%H:%M:%S")
                        await client.reply(dot_id, f"@{username} الان ساعت {now} هست ⏰")
                        print(f"   ⏰ Replied: time")

                    elif "پینگ" in content:
                        await client.reply(dot_id, f"@{username} Pong! 🏓")
                        print(f"   🏓 Replied: ping")

                    elif "راهنما" in content:
                        await client.reply(
                            dot_id,
                            f"@{username} من می‌تونم:\n"
                            "👋 سلام\n⏰ ساعت\n🏓 پینگ\n📈 ترند\n📰 فید\n🤖 بات"
                        )
                        print(f"   📖 Replied: help")

                    elif "ترند" in content:
                        trends = await client.get_trending_hashtags()
                        top5 = trends[:5]
                        text = f"@{username} هشتگ‌های ترند:\n"
                        for t in top5:
                            name = t.get("name", t.get("tag", "?"))
                            text += f"   #{name}\n"
                        await client.reply(dot_id, text)
                        print(f"   📈 Replied: trends")

                    elif "فید" in content:
                        feed = await client.home_feed(3)
                        text = f"@{username} آخرین پست‌ها:\n"
                        for item in feed.get("results", []):
                            a = item.get("author", {})
                            c = item.get("content", "")[:40]
                            text += f"   @{a.get('username', '?')}: {c}...\n"
                        await client.reply(dot_id, text)
                        print(f"   📰 Replied: feed")

                    else:
                        await client.reply(
                            dot_id,
                            f"@{username} سلام! من باتم 🤖\nبگو 'راهنما'!"
                        )
                        print(f"   💬 Replied: default")

                await asyncio.sleep(15)

            except KeyboardInterrupt:
                print("\n👋 Bot stopped")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                await asyncio.sleep(15)


if __name__ == "__main__":
    print("🚀 aiodot Echo Bot\n")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")