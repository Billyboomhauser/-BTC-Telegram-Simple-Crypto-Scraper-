import asyncio
import re
from telethon import TelegramClient, errors

API_ID = #enter value
API_HASH = #enter value

BTC_PATTERN = r'\b(1[a-km-zA-HJ-NP-Z1-9]{25,34}|3[a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[ac-hj-np-z02-9]{11,71})\b'


async def main():
    client = TelegramClient('investigator_session', API_ID, API_HASH)

    print("[*] Connecting to Telegram...")
    await client.start()

    if not await client.is_user_authorized():
        print("[-] Verification failed.")
        return

    print("[+] Successfully connected!")

    target_group = '@Whale_Alert'
    limit = 300

    try:
        print(f"[*] Scanning last {limit} messages in {target_group}...")
        async for message in client.iter_messages(target_group, limit=limit):
            if message.text:
                matches = re.findall(BTC_PATTERN, message.text)
                if matches:
                    print(f"\n[!] ALERT: Crypto address found in Message ID {message.id}")
                    print(f"    Sender ID: {message.sender_id}")
                    print(f"    Addresses: {set(matches)}")
                    print(f"    Text snippet: {message.text[:300]}...")

        print("\n[*] Scan complete.")

    except errors.FloodWaitError as e:
        print(f"[-] Rate limited! Must wait {e.seconds} seconds.")
    except Exception as e:
        print(f"[-] An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())