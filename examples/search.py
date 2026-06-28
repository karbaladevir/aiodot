"""aiodot - Search users and explore trending content."""

import asyncio
from aiodot import MyDotClient

USERNAME = ""
PASSWORD = ""


async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login(USERNAME, PASSWORD)

        print("🔍 Searching for 'ali'...")
        results = await client.search_users("ali")

        if isinstance(results, dict):
            users = results.get("results", [])
        else:
            users = results

        print(f"   Found {len(users)} users:")
        for u in users[:5]:
            print(f"   @{u.get('username', '?')} - {u.get('display_name', '')}")

        print("\n📈 Trending Hashtags:")
        trends = await client.get_trending_hashtags()
        for t in trends[:10]:
            name = t.get("name", t.get("tag", "?"))
            print(f"   #{name}")

        print("\n🖼️ Trending Media:")
        media = await client.get_trending_media(5)
        print(f"   {media.get('count', 0)} items")


asyncio.run(main())