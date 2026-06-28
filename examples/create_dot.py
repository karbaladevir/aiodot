import asyncio
from aiodot import MyDotClient

USERNAME = ""
PASSWORD = ""


async def main():
    async with MyDotClient(session_file="session.json") as client:
        await client.login(USERNAME, PASSWORD)

        me = await client.get_me()
        print(f"Welcome @{me.username}")

        dot = await client.create_dot("Hello MyDot!")
        print(f"Post sent: {dot.url}")


if __name__ == "__main__":
    asyncio.run(main())