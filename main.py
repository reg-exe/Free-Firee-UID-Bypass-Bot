import discord
from discord import app_commands
import requests
import os
import json
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# ============================
# ENVIRONMENT SETUP
# ============================
if os.path.exists('.env'):
    load_dotenv()

JSONBIN_URL = os.getenv("JSONBIN_URL")
JSONBIN_API_KEY = os.getenv("JSONBIN_API_KEY")
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))
DEV_ID = int(os.getenv("DEV_DISCORD_ID", "0"))
ALLOWED_CHANNEL = int(os.getenv("ALLOWED_CHANNEL", "0"))

# Validate required environment variables
required_vars = {
    "JSONBIN_URL": JSONBIN_URL,
    "JSONBIN_API_KEY": JSONBIN_API_KEY,
    "DISCORD_BOT_TOKEN": BOT_TOKEN
}

missing_vars = [var for var, value in required_vars.items() if not value]
if missing_vars:
    raise Exception(f"Missing environment variables: {', '.join(missing_vars)}")

JSONBIN_HEADERS = {
    "Content-Type": "application/json",
    "X-Master-Key": JSONBIN_API_KEY,
    "X-Bin-Meta": "false"
}

WHITELIST_PAUSED = False

# ============================
# JSONBIN.IO FUNCTIONS (UPDATED FOR ARRAY STRUCTURE)
# ============================
def get_whitelist_data():
    """Fetch whitelist data from JSONBin.io"""
    try:
        response = requests.get(JSONBIN_URL, headers=JSONBIN_HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Ensure we always return an array
            if isinstance(data, list):
                return data
            else:
                return []
        else:
            print(f"Error fetching data: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching from JSONBin: {e}")
        return []

def update_whitelist_data(data):
    """Update whitelist data on JSONBin.io"""
    try:
        response = requests.put(JSONBIN_URL, headers=JSONBIN_HEADERS, json=data, timeout=10)
        return response.status_code == 200
    except Exception as e:
        print(f"Error updating JSONBin: {e}")
        return False

def get_uid_entry(uid):
    """Get specific UID entry from whitelist"""
    data = get_whitelist_data()
    for entry in data:
        if entry.get("uid") == uid:
            return entry
    return None

def add_uid_entry(uid, expiry, comment):
    """Add or update UID entry"""
    data = get_whitelist_data()
    
    # Check if UID already exists
    existing_index = -1
    for i, entry in enumerate(data):
        if entry.get("uid") == uid:
            existing_index = i
            break
    
    new_entry = {
        "uid": uid,
        "expiry_date": expiry,
        "comment": comment
    }
    
    if existing_index >= 0:
        # Update existing entry
        data[existing_index] = new_entry
    else:
        # Add new entry
        data.append(new_entry)
    
    return update_whitelist_data(data)

def remove_uid_entry(uid):
    """Remove UID entry"""
    data = get_whitelist_data()
    new_data = [entry for entry in data if entry.get("uid") != uid]
    
    if len(new_data) != len(data):
        return update_whitelist_data(new_data)
    return False

def get_all_uids():
    """Get all UID entries"""
    return get_whitelist_data()

# ============================
# ENHANCED LOGGING SYSTEM
# ============================
async def send_log(bot, action: str, uid: str, user: discord.User, expiry: str = None, comment: str = None):
    """Enhanced logging function with formatted messages"""
    if not LOG_CHANNEL_ID:
        return
        
    ch = bot.get_channel(LOG_CHANNEL_ID)
    if not ch:
        return

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create formatted log message based on action type
    if action == "ADD":
        embed = discord.Embed(
            title="🟢 UID ADDED",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="UID", value=f"`{uid}`", inline=True)
        embed.add_field(name="Expiry", value=f"`{expiry}`", inline=True)
        embed.add_field(name="Comment", value=f"`{comment}`", inline=True)
        embed.add_field(name="Added By", value=f"`{user.name}`\n(`{user.id}`)", inline=True)
        embed.add_field(name="Timestamp", value=f"`{current_time}`", inline=True)
        embed.set_footer(text="Whitelist System")
        
    elif action == "REMOVE":
        embed = discord.Embed(
            title="🔴 UID REMOVED",
            color=0xff0000,
            timestamp=datetime.now()
        )
        embed.add_field(name="UID", value=f"`{uid}`", inline=True)
        embed.add_field(name="Removed By", value=f"`{user.name}`\n(`{user.id}`)", inline=True)
        embed.add_field(name="Timestamp", value=f"`{current_time}`", inline=True)
        embed.set_footer(text="Whitelist System")
        
    elif action == "PAUSE":
        embed = discord.Embed(
            title="⏸️ SYSTEM PAUSED",
            color=0xffff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="Action By", value=f"`{user.name}`\n(`{user.id}`)", inline=True)
        embed.add_field(name="Timestamp", value=f"`{current_time}`", inline=True)
        embed.set_footer(text="Whitelist System")
        
    elif action == "RESUME":
        embed = discord.Embed(
            title="▶️ SYSTEM RESUMED",
            color=0x00ff00,
            timestamp=datetime.now()
        )
        embed.add_field(name="Action By", value=f"`{user.name}`\n(`{user.id}`)", inline=True)
        embed.add_field(name="Timestamp", value=f"`{current_time}`", inline=True)
        embed.set_footer(text="Whitelist System")
    
    await ch.send(embed=embed)

async def send_simple_log(bot, message: str):
    """Simple text-based log for non-UID actions"""
    if not LOG_CHANNEL_ID:
        return
        
    ch = bot.get_channel(LOG_CHANNEL_ID)
    if ch:
        await ch.send(f"`{datetime.now().strftime('%H:%M:%S')}` {message}")

# ============================
# FORMAT DATE FOR DISPLAY
# ============================
def format_display_date(raw):
    """Format date from YYYY-MM-DD to DD-MM-YYYY for display"""
    try:
        y, m, d = raw.split("-")
        return f"{d}-{m}-{y}"
    except:
        return raw

# ============================
# OWNER CHECK
# ============================
def owner_only():
    async def predicate(interaction):
        if interaction.user.id != DEV_ID:
            await interaction.response.send_message(
                "❌ Only the **bot owner** can use this command.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

# ============================
# CHANNEL CHECK
# ============================
def channel_only():
    async def predicate(interaction):
        if interaction.channel_id != ALLOWED_CHANNEL:
            await interaction.response.send_message(
                "❌ You can only use commands in the assigned whitelist channel.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

# ============================
# PAUSE CHECK
# ============================
def pause_check():
    async def predicate(interaction):
        if WHITELIST_PAUSED:
            await interaction.response.send_message(
                "⚠️ Whitelist system is currently **PAUSED**.",
                ephemeral=True
            )
            return False
        return True
    return app_commands.check(predicate)

# ============================
# FORMAT DATE
# ============================
def format_box_date(raw):
    try:
        y, m, d = raw.split("-")
        return f"{d} - {m} - {y}"
    except:
        return raw

# ============================
# BOT CLASS
# ============================
class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f"[READY] Logged in as {self.user}")
        try:
            cmds = await self.tree.sync()
            print(f"Synced {len(cmds)} commands.")
            # Send startup log
            await send_simple_log(self, "🟢 **Bot Started Successfully**")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def setup_hook(self):
        print("[SETUP] Bot is starting up...")

bot = MyBot()

# ============================
# /help (PUBLIC)
# ============================
@bot.tree.command(name="help", description="Show all bot commands")
@channel_only()
async def help_cmd(interaction: discord.Interaction):
    text = (
        "**📘 Whitelist Bot Commands**\n\n"
        "🔵 Public:\n"
        "`/help`\n"
        "`/checkuid <uid>`\n"
        "`/viewuid <uid>`\n"
        "`/listuids`\n"
        "`/adduid <uid> <year> <month> <day> <comment>`\n\n"
        "🟣 Owner Only:\n"
        "`/removeuid <uid>`\n"
        "`/pause`\n"
        "`/resume`\n"
    )
    await interaction.response.send_message(text)

# ============================
# /checkuid (PUBLIC)
# ============================
@bot.tree.command(name="checkuid", description="Check UID JSON")
@channel_only()
async def checkuid(interaction: discord.Interaction, uid: str):
    try:
        entry = get_uid_entry(uid)
        if not entry:
            await interaction.response.send_message("UID not found.")
            return

        formatted = [{
            "uid": entry["uid"],
            "expiry_date": entry["expiry_date"],
            "comment": entry["comment"]
        }]

        await interaction.response.send_message(
            f"```json\n{json.dumps(formatted, indent=2)}\n```"
        )
    except Exception as e:
        await interaction.response.send_message("❌ Database connection error.")
        return

# ============================
# /viewuid (PUBLIC)
# ============================
@bot.tree.command(name="viewuid", description="UID box view")
@channel_only()
async def viewuid(interaction: discord.Interaction, uid: str):
    try:
        entry = get_uid_entry(uid)
        if not entry:
            await interaction.response.send_message("UID not found.")
            return

        pretty = format_box_date(entry["expiry_date"])

        box = (
            "```\n"
            "📦 WHITELIST ENTRY\n"
            "──────────────────────────\n"
            f"UID:        {entry['uid']}\n"
            f"Expiry:     {pretty}\n"
            f"Comment:    {entry['comment']}\n"
            "```"
        )
        await interaction.response.send_message(box)
    except Exception as e:
        await interaction.response.send_message("❌ Database connection error.")
        return

# ============================
# /listuids (PUBLIC)
# ============================
@bot.tree.command(name="listuids", description="List all UIDs")
@channel_only()
async def listuids(interaction: discord.Interaction):
    try:
        data = get_all_uids()
        formatted = [{
            "uid": entry["uid"],
            "expiry_date": entry["expiry_date"],
            "comment": entry["comment"]
        } for entry in data]

        await interaction.response.send_message(
            f"```json\n{json.dumps(formatted, indent=2)}\n```"
        )
    except Exception as e:
        await interaction.response.send_message("❌ Database connection error.")
        return

# ============================
# /adduid (PUBLIC) - UPDATED FOR JSONBIN ARRAY
# ============================
@bot.tree.command(name="adduid", description="Add a UID entry")
@channel_only()
@pause_check()
async def adduid(
    interaction: discord.Interaction,
    uid: str,
    year: int,
    month: int,
    day: int,
    comment: str
):
    expiry = f"{year:04d}-{month:02d}-{day:02d}"
    
    try:
        # Check if UID already exists
        existing_entry = get_uid_entry(uid)
        
        if existing_entry:
            action = "updated"
        else:
            action = "added"
        
        # Add/update UID
        success = add_uid_entry(uid, expiry, comment)
        
        if success:
            # Send simple confirmation message ONLY to the user who added (ephemeral)
            if action == "added":
                await interaction.response.send_message(f"🟢 UID **{uid}** added.", ephemeral=True)
            else:
                await interaction.response.send_message(f"🟡 UID **{uid}** updated.", ephemeral=True)
            
            # Send detailed log to log channel (visible to everyone in log channel)
            await send_log(bot, "ADD", uid, interaction.user, expiry, comment)
        else:
            await interaction.response.send_message("❌ Error saving UID to database.", ephemeral=True)
            
    except Exception as e:
        await interaction.response.send_message("❌ Database connection error.", ephemeral=True)
        return

# ============================
# /removeuid (OWNER ONLY) - UPDATED FOR JSONBIN ARRAY
# ============================
@bot.tree.command(name="removeuid", description="Remove a UID")
@channel_only()
@owner_only()
@pause_check()
async def removeuid(interaction: discord.Interaction, uid: str):
    try:
        success = remove_uid_entry(uid)
        
        if success:
            # Send confirmation only to the user who removed
            await interaction.response.send_message(f"🔴 UID **{uid}** removed.", ephemeral=True)
            # Send log to log channel
            await send_log(bot, "REMOVE", uid, interaction.user)
        else:
            await interaction.response.send_message("❌ UID not found or error removing.", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message("❌ Database connection error.", ephemeral=True)
        return

# ============================
# /pause (OWNER ONLY)
# ============================
@bot.tree.command(name="pause", description="Pause whitelist")
@channel_only()
@owner_only()
async def pause(interaction: discord.Interaction):
    global WHITELIST_PAUSED
    WHITELIST_PAUSED = True
    
    # Send confirmation only to the user
    await interaction.response.send_message("⏸️ Whitelist PAUSED.", ephemeral=True)
    # Send log to log channel
    await send_log(bot, "PAUSE", "", interaction.user)

# ============================
# /resume (OWNER ONLY)
# ============================
@bot.tree.command(name="resume", description="Resume whitelist")
@channel_only()
@owner_only()
async def resume(interaction: discord.Interaction):
    global WHITELIST_PAUSED
    WHITELIST_PAUSED = False
    
    # Send confirmation only to the user
    await interaction.response.send_message("▶️ Whitelist RESUMED.", ephemeral=True)
    # Send log to log channel
    await send_log(bot, "RESUME", "", interaction.user)

# ============================
# RUN BOT
# ============================
if __name__ == "__main__":
    bot.run(BOT_TOKEN)
