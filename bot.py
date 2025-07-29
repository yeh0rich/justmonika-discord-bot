import os
import random
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Glitch event functions
async def glitch_channel_name(guild: discord.Guild):
    """Temporarily rename a channel to '𝔾𝕝𝕚𝕥𝕔𝕙𝕖𝕕-' + original name"""
    channel = random.choice([c for c in guild.text_channels if c.permissions_for(guild.me).manage_channels])
    original_name = channel.name
    glitched_name = f"𝔾𝕝𝕚𝕥𝕔𝕙𝕖𝕕-{original_name}"
    try:
        await channel.edit(name=glitched_name)
        await asyncio.sleep(random.randint(10, 30))  # Glitch lasts 10-30s
        await channel.edit(name=original_name)
    except Exception:
        pass

async def glitch_ping_user(guild: discord.Guild):
    """Randomly ping a user with a creepy message"""
    members = [m for m in guild.members if not m.bot and m.status != discord.Status.offline]
    if not members:
        return
    user = random.choice(members)
    channel = random.choice([c for c in guild.text_channels if c.permissions_for(guild.me).send_messages])
    creepy_messages = [
        "You can't trust them.",
        "Are you alone?",
        "She's watching.",
        "Don't look behind you.",
        "Why are you still here?"
    ]
    try:
        await channel.send(f"{user.mention} {random.choice(creepy_messages)}")
    except Exception:
        pass

async def glitch_typing_event(guild: discord.Guild):
    """Bot types then sends a corrupted message"""
    channel = random.choice([c for c in guild.text_channels if c.permissions_for(guild.me).send_messages])
    corrupted_msgs = [
        ".chr file corrupted...",
        "Reality is breaking...",
        "Error: 0x0001F4A9",
        "[DATA EXPUNGED]",
        "Monika is here."
    ]
    try:
        async with channel.typing():
            await asyncio.sleep(random.randint(2, 5))
        await channel.send(random.choice(corrupted_msgs))
    except Exception:
        pass

async def glitch_nickname(guild: discord.Guild):
    """Temporarily change a random member's nickname to a glitched 'JustMonika.'"""
    candidates = [m for m in guild.members if not m.bot and m != guild.me and guild.me.top_role > m.top_role and m.nick != "JustMonika."]
    if not candidates:
        return
    user = random.choice(candidates)
    glitched_nick = "JυѕтMσηιкα."  # Unicode-glitched JustMonika.
    try:
        original_nick = user.nick
        await user.edit(nick=glitched_nick)
        await asyncio.sleep(random.randint(30, 60))
        await user.edit(nick=original_nick)
    except Exception:
        pass

async def trigger_random_glitch(guild: discord.Guild):
    """Trigger a random glitch event"""
    glitch_funcs = [glitch_channel_name, glitch_ping_user, glitch_typing_event, glitch_nickname]
    await random.choice(glitch_funcs)(guild)

# Simple test command
@bot.tree.command(name="test", description="Test if the bot is working")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("JustMonika.exe is working! 🧠", ephemeral=True)

# Glitch command
@bot.tree.command(name="glitch", description="Trigger a glitch event (admin only)")
@app_commands.checks.has_permissions(administrator=True)
async def glitch(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("𝔾𝕝𝕚𝕥𝕔𝕙 𝕖��𝕖𝕟𝕥 𝕥𝕣𝕚𝕘𝕘𝕖𝕕!", ephemeral=True)
        
        # Randomly choose a glitch event
        import random
        event = random.choice([
            glitch_channel_name,
            glitch_ping_user,
            glitch_typing_event,
            glitch_nickname
        ])
        
        await event(interaction.guild)
        
    except Exception as e:
        await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)

@glitch.error
async def glitch_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

@bot.tree.command(name="monikanick", description="Change someone's nickname to 'Just Monika.' (admin only)")
@app_commands.describe(user="The user to monikafy. If not set, picks a random member.")
@app_commands.checks.has_permissions(administrator=True)
async def monikanick(interaction: discord.Interaction, user: discord.Member = None):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    if user is None:
        candidates = [m for m in guild.members if not m.bot]
        if not candidates:
            await interaction.followup.send("No valid members to monikafy!", ephemeral=True)
            return
        user = random.choice(candidates)
    # Removed bot/self and role hierarchy checks for full testability
    try:
        original_nick = user.nick
        await user.edit(nick="Just Monika.")
        await interaction.followup.send(f"{user.mention} is now Just Monika. (Will revert in 60s)", ephemeral=True)
        await asyncio.sleep(60)
        await user.edit(nick=original_nick)
    except discord.Forbidden:
        await interaction.followup.send("I don't have permission to change that user's nickname.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@monikanick.error
async def monikanick_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

@bot.tree.command(name="monikasay", description="Make JM.exe say anything (admin only)")
@app_commands.describe(message="The message for Monika to say.")
@app_commands.checks.has_permissions(administrator=True)
async def monikasay(interaction: discord.Interaction, message: str):
    await interaction.response.defer(ephemeral=True)
    try:
        await interaction.channel.send(message)
        await interaction.followup.send("Message sent as JM.exe!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@monikasay.error
async def monikasay_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred.", ephemeral=True)

@bot.tree.command(name="monikadm", description="Send a DM as Monika to a user (admin only)")
@app_commands.describe(user="The user to DM", message="The message to send")
@app_commands.checks.has_permissions(administrator=True)
async def monikadm(interaction: discord.Interaction, user: discord.Member, message: str):
    try:
        await user.send(message)
        await interaction.response.send_message(f"✅ DM sent to {user.display_name}.", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message(f"❌ Could not DM {user.display_name} (DMs closed or privacy settings).", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {e}", ephemeral=True)

# Bot events
@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s) to Discord.")
        # Force global resync to clear out old command versions
        await bot.tree.sync()
        print("Forced global command resync.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Main entrypoint
if __name__ == "__main__":
    print("Starting fresh JustMonika.exe bot...")
    
    try:
        bot.run(os.getenv("TOKEN"))
    except Exception as e:
        print(f"Error starting bot: {e}") 