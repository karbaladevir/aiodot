"""aiodot - Get profile and create test dot."""

import asyncio
from aiodot import MyDotClient

USERNAME = ""
PASSWORD = ""


async def main():
    async with MyDotClient(session_file="session.json") as c:
        await c.login(USERNAME, PASSWORD)

        me = await c.get_me()
        print(f"✅ @{me.username}: {me.display_name}")

        dot = await c.create_dot("Test from aiodot! 🚀")
        print(f"📝 {dot.url}")


asyncio.run(main())