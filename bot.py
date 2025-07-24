import os
import random
import asyncio
import discord
from discord.ext import commands, tasks
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Glitch Event Functions ---
async def glitch_channel_name(guild: discord.Guild):
    channel = random.choice([c for c in guild.text_channels if c.permissions_for(guild.me).manage_channels])
    original_name = channel.name
    glitched_name = "𝔾𝕝𝕚𝕥𝕔𝕙𝕖𝕕-" + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=4))
    try:
        await channel.edit(name=glitched_name)
        await asyncio.sleep(random.randint(10, 30))  # Glitch lasts 10-30s
        await channel.edit(name=original_name)
    except Exception:
        pass

async def glitch_ping_user(guild: discord.Guild):
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

async def trigger_random_glitch(guild: discord.Guild):
    glitch_funcs = [glitch_channel_name, glitch_ping_user, glitch_typing_event]
    await random.choice(glitch_funcs)(guild)

# --- Background Task for Rare Glitches ---
@tasks.loop(seconds=3600)  # Check every hour
async def rare_glitch_task():
    await bot.wait_until_ready()
    for guild in bot.guilds:
        # 10% chance per hour per guild
        if random.random() < 0.1:
            await trigger_random_glitch(guild)

# --- Slash Command Setup ---
class Glitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        rare_glitch_task.start()

    @app_commands.command(name="glitch", description="Trigger a random glitch event (admin only)")
    @app_commands.checks.has_permissions(administrator=True)
    async def glitch(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        await trigger_random_glitch(interaction.guild)
        await interaction.followup.send("Glitch event triggered!", ephemeral=True)

    @glitch.error
    async def glitch_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred.", ephemeral=True)

    @app_commands.command(name="monikanick", description="Change someone's nickname to 'Just Monika.' (admin only)")
    @app_commands.describe(user="The user to monikafy. If not set, picks a random member.")
    @app_commands.checks.has_permissions(administrator=True)
    async def monikanick(self, interaction: discord.Interaction, user: discord.Member = None):
        await interaction.response.defer(ephemeral=True)
        guild = interaction.guild
        if user is None:
            candidates = [m for m in guild.members if not m.bot and m != guild.me and m.top_role < guild.me.top_role]
            if not candidates:
                await interaction.followup.send("No valid members to monikafy!", ephemeral=True)
                return
            user = random.choice(candidates)
        if user.bot or user == guild.me or user.top_role >= guild.me.top_role:
            await interaction.followup.send("Cannot monikafy this user.", ephemeral=True)
            return
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
    async def monikanick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred.", ephemeral=True)

    @app_commands.command(name="fakedelete", description="Pretend to delete a channel, role, or file (admin only)")
    @app_commands.describe(target="Channel, role, or file name to fake-delete.")
    @app_commands.checks.has_permissions(administrator=True)
    async def fakedelete(self, interaction: discord.Interaction, target: str):
        await interaction.response.defer()
        guild = interaction.guild
        channel = None
        role = None
        # Try to resolve channel
        if target.startswith("<#") and target.endswith(">"):
            try:
                channel_id = int(target[2:-1])
                channel = guild.get_channel(channel_id)
            except:
                pass
        # Try to resolve role
        elif target.startswith("<@&") and target.endswith(">"):
            try:
                role_id = int(target[3:-1])
                role = guild.get_role(role_id)
            except:
                pass
        # Try to resolve by name
        if not channel and not role:
            channel = discord.utils.get(guild.text_channels, name=target.replace("#", ""))
            role = discord.utils.get(guild.roles, name=target.replace("@", ""))
        # Determine type
        if channel:
            display = f"#{channel.name}"
        elif role:
            display = f"@{role.name}"
        else:
            display = target
        # Progress bar animation
        progress_states = [
            "[░░░░░░░░░░] 0%",
            "[▓░░░░░░░░░] 10%",
            "[▓▓░░░░░░░░] 20%",
            "[▓▓▓░░░░░░░] 30%",
            "[▓▓▓▓░░░░░░] 40%",
            "[▓▓▓▓▓░░░░░] 50%",
            "[▓▓▓▓▓▓░░░░] 60%",
            "[▓▓▓▓▓▓▓░░░] 70%",
            "[▓▓▓▓▓▓▓▓░░] 80%",
            "[▓▓▓▓▓▓▓▓▓░] 90%",
            "[▓▓▓▓▓▓▓▓▓▓] 100%"
        ]
        msg = await interaction.followup.send(f"Deleting {display}... {progress_states[0]}")
        for state in progress_states[1:]:
            await asyncio.sleep(random.uniform(0.3, 0.7))
            await msg.edit(content=f"Deleting {display}... {state}")
        # Glitchy ending
        endings = [
            f"Error: Unable to delete {display}. Reality is protected.",
            f"{display} has been deleted. (just kidding!)",
            f"[GLITCH] {display} not found.",
            f"{display} has become corrupted...",
            f"Monika: Did you really think I'd let you do that?"
        ]
        await asyncio.sleep(1)
        await msg.edit(content=random.choice(endings))
    
    @fakedelete.error
    async def fakedelete_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message("You need to be an admin to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An error occurred.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Glitch(bot))

# --- Main Entrypoint ---
import asyncio

async def main():
    async with bot:
        await bot.load_extension("bot")
        await bot.start(os.environ["TOKEN"])

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        # For environments like Replit/Jupyter that already have a running loop
        if "already running" in str(e):
            import nest_asyncio
            nest_asyncio.apply()
            loop = asyncio.get_running_loop()
            loop.create_task(main())
        else:
            raise e 