import asyncio
from aiodot import MyDotClient

USERNAME = ""
PASSWORD = ""
TARGET_USERNAME = ""


async def chat_example():
    async with MyDotClient(session_file="chat_session.json") as client:
        await client.login(USERNAME, PASSWORD)

        me = await client.get_me()
        print(f"Logged in as: @{me.username}")

        unread = await client.get_unread_count()
        print(f"Unread messages: {unread}")

        convs = await client.get_conversations(tab="all", limit=10)
        print(f"Conversations: {len(convs.get('conversations', []))}")

        if not convs.get("conversations"):
            print("No conversations found. Starting new chat...")
            users = await client.search_users(TARGET_USERNAME)
            if not users.get("results"):
                print("User not found")
                return
            target = users["results"][0]
            conv = await client.get_conversation(target["id"])
            conv_id = conv["id"]
        else:
            conv_id = convs["conversations"][0]["id"]

        await client.send_message(conv_id, "Hello from aiodot!")
        print("Message sent!")

        msgs = await client.get_messages(conv_id, limit=20)
        print(f"Last {len(msgs.get('messages', []))} messages:")

        for msg in msgs.get("messages", [])[:5]:
            sender = msg.get("sender", {}).get("username", "unknown")
            content = msg.get("content", "")[:50]
            print(f"  @{sender}: {content}")

        await client.mark_conversation_read(conv_id)
        print("Conversation marked as read")

        status = await client.get_connection_status()
        print(f"Chat status: {status.get('status', 'unknown')}")


if __name__ == "__main__":
    asyncio.run(chat_example())