import discord
from discord.ext import commands, tasks
import random
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

GLITCH_MESSAGES = [
    "You can't trust them.",
    "Are you alone?",
    "Why are you still here?",
    "Just Monika.",
    "I see you.",
    "Don't look behind you...",
    "Everything is fine. Probably."
]

META_QUOTES = [
    "Did you ever wonder if you're being watched?",
    "This isn't just a game...",
    "I know you're there, [user].",
    "Sometimes, reality glitches.",
    "You can't escape me."
]

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    glitch_event.start()
    meta_quote_event.start()

@tasks.loop(minutes=10)
async def glitch_event():
    channels = [c for c in bot.get_all_channels() if isinstance(c, discord.TextChannel)]
    if channels:
        channel = random.choice(channels)
        await channel.send(random.choice(GLITCH_MESSAGES))

@tasks.loop(minutes=30)
async def meta_quote_event():
    channels = [c for c in bot.get_all_channels() if isinstance(c, discord.TextChannel)]
    if channels:
        channel = random.choice(channels)
        await channel.send(random.choice(META_QUOTES))

bot.run("REDACTED") 
# Dummy commit to move HEAD
