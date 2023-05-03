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
            if birthdays[today]:
                message_author = await client.fetch_user(int(owner_id))
                channels = client.get_channel(int(owner_ch))
                if channels is not None:
                    for birthday in birthdays[today]:
                        await channels.send(f"Happy Birthday to {birthday} :partying_face: ")
                        await message_author.send(f"It is  {birthday}'s Birthday!")

        await asyncio.sleep(60)


@client.event
async def on_message(message):
    if message.content.startswith("!add") and message.author.guild_permissions.administrator:
        parts = message.content.split()
        words = parts[1]
        if not words.isnumeric() or len(parts) != int(words) + 3:
            await message.channel.send("Invalid syntax. Use: `!add <words_in_name> <name> <date>`")
            return

        fullname = ""
        for name in range(2, len(parts)-1):
            fullname += parts[name]+" "
            fullname.strip()
        date = parts[len(parts)-1]
        if date not in birthdays:
            birthdays[date] = []
            birthdays[date].append(fullname)
        else:
            birthdays[date].append(fullname)
        with open("birthdays.json", "w") as f:
            json.dump(birthdays, f, indent=4)

        await message.channel.send(f"{fullname}'s birthday added.")

    elif message.content == "!list":
        if not birthdays:
            await message.channel.send("No birthdays added.")
        else:
            response = "Birthdays:\n"
            for date, name in birthdays.items():
                if name:
                    list_of_name = ', '.join(name)
                    response += f"{list_of_name} : {date}\n"
            await message.channel.send(response)

    elif message.content.startswith("!remove") and message.author.guild_permissions.administrator:
        parts = message.content.split()
        words = parts[1]
        if not words.isnumeric() or len(parts) != int(words) + 3:
            await message.channel.send("Invalid syntax. Use: `!remove <words_in_name> <name> <date>`")
            return

        fullname = ""
        for name in range(2, len(parts)-1):
            fullname += parts[name]+" "
            fullname.strip()
        date = parts[len(parts)-1]
        for dates, names in birthdays.items():
            if fullname in names and dates == date:
                names.remove(fullname)
                with open("birthdays.json", "w") as f:
                    json.dump(birthdays, f, indent=4)
                await message.channel.send(f"{fullname}'s birthdays removed.")
                break
        else:
            await message.channel.send(f"{fullname}'s birthday not found.")

    elif message.content == "!today":
        today = datetime.now().strftime("%m-%d")
        if birthdays[today]:
            for birthday in birthdays[today]:
                await message.channel.send(f"It is {birthday}'s Birthday!")
        else:
            await message.channel.send("No birthdays today.")

with open("token.txt", "r") as f:
    token = f.read().strip()

loop = asyncio.get_event_loop()
loop.create_task(client.start(token))
loop.create_task(check_birthdays())
loop.run_forever()
