"""aiodot - Auto update avatar from proxy every 30 seconds."""

import asyncio
import aiohttp
from aiodot import MyDotClient

USERNAME = " "
PASSWORD = " "
PROXY_URL = "http://formessage.com/crosproxy2.php"


async def fetch_image(session: aiohttp.ClientSession) -> bytes:
    async with session.get(PROXY_URL) as resp:
        return await resp.read()


async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login(USERNAME, PASSWORD)
        print(f"✅ @{(await client.get_me()).username}")

        async with aiohttp.ClientSession() as http:
            while True:
                try:
                    image_data = await fetch_image(http)
                    with open("avatar.jpg", "wb") as f:
                        f.write(image_data)

                    avatar_key = await client.upload_avatar("avatar.jpg", "avatar.jpg", "image/jpeg")
                    if avatar_key:
                        await client.update_profile(avatar_key=avatar_key)
                        print(f"🔄 Avatar updated!")

                except Exception as e:
                    print(f"❌ Error: {e}")

                await asyncio.sleep(30)


if __name__ == "__main__":
    asyncio.run(main())