import discord
import json
from datetime import datetime, time
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

with open("birthdays.json", "r") as f:
    birthdays = json.load(f)

with open('owner_id.txt', 'r') as f:
    owner_id = f.read().strip()

with open('owner_ch.txt', 'r') as f:
    owner_ch = f.read().strip()


@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    message_author = await client.fetch_user(int(owner_id))
    await message_author.send("Bot is Online!")


@client.event
async def check_birthdays():
    await client.wait_until_ready()
    today = ""
    while True:
        with open("birthdays.json", "r") as f:
            birthdays = json.load(f)
        now = datetime.now()
        date = now.strftime("%m-%d")
        if date != today:
            today = date
            birthday_today = [name for name,
                              date in birthdays.items() if date == today]
            if birthday_today:
                message_author = await client.fetch_user(int(owner_id))
                channels = client.get_channel(int(owner_ch))
                if channels is not None:
                    await channels.send(f"Happy Birthday to {' '.join(birthday_today)} :partying_face: ")
                    await message_author.send(f"It is {' '.join(birthday_today)}'s Birthday!")

        await asyncio.sleep(60)


@client.event
async def on_message(message):
    if message.content.startswith("!add") and message.author.guild_permissions.administrator:
        parts = message.content.split()
        if len(parts) != 3:
            await message.channel.send("Invalid syntax. Use: `!add <name> <date>`")
            return

        name = parts[1]
        date = parts[2]

        birthdays[name] = date
        with open("birthdays.json", "w") as f:
            json.dump(birthdays, f)

        await message.channel.send(f"{name}'s birthday added.")

    elif message.content == "!list":
        if not birthdays:
            await message.channel.send("No birthdays added.")
        else:
            response = "Birthdays:\n"
            for name, date in birthdays.items():
                response += f"{name}: {date}\n"
            await message.channel.send(response)

    elif message.content.startswith("!remove") and message.author.guild_permissions.administrator:
        parts = message.content.split()
        if len(parts) != 2:
            await message.channel.send("Invalid syntax. Use: `!remove <name>`")
            return

        name = parts[1]
        if name in birthdays:
            del birthdays[name]
            with open("birthdays.json", "w") as f:
                json.dump(birthdays, f)
            await message.channel.send(f"{name}'s birthday removed.")
        else:
            await message.channel.send(f"{name}'s birthday not found.")

    elif message.content == "!today":
        today = datetime.now().strftime("%m-%d")
        today_birthdays = [name for name,
                           date in birthdays.items() if date == today]
        if today_birthdays:
            await message.channel.send(f"It is {' '.join(today_birthdays)}'s Birthday!")
        else:
            await message.channel.send("No birthdays today.")

with open("token.txt", "r") as f:
    token = f.read().strip()

loop = asyncio.get_event_loop()
loop.create_task(client.start(token))
loop.create_task(check_birthdays())
loop.run_forever()
