# This example requires the 'message_content' intent.
import discord
import os
from db import get_reply, connect

# my own scuffed .env parser
with open(".env", "r") as f:
    for line in f.read().strip().splitlines():
        env, value = line.split('=')
        os.environ[env] = value

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Initialize discord API
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Connect to sqlite3
sqlite_db = connect("chat.db")


@client.event
async def on_ready():
    print(f'[SYSTEM] We have logged in as {client.user}')

@client.event
async def on_message(message):
    """Generates a response for each @, reply or DM."""
    if message.author == client.user:
        return
    is_dm = isinstance(message.channel, discord.DMChannel)
    if len(message.mentions) or is_dm:
        if (client.user.id in map(lambda msg: msg.id, message.mentions)) or is_dm:
            print(f"[{message.author}]: asks \"{message.clean_content}\"")
            # should be slow, but I don't care 😎
            reply = await get_reply(sqlite_db, message.clean_content, message.author.id, OPENAI_KEY)
            print(f"[{client.user}]: {reply}")
            await message.reply(reply)


client.run(os.getenv('DISCORD_TOKEN'))
