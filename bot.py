import discord
import requests
import asyncio
import os
from discord.ext import tasks, commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Your bot token
GITHUB_REPO = "ShadowCCS/Flashcards"  # GitHub repository
CHANNEL_ID = 123456789012345678  # Replace with your Discord channel ID

# Intent settings
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)
latest_release = None  # Store latest release version

async def check_github_release():
    global latest_release
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        new_version = data["tag_name"]
        
        if latest_release is None:
            latest_release = new_version  # Set initial version
        elif new_version != latest_release:
            latest_release = new_version  # Update latest release
            channel = bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"🚀 New release detected: **{new_version}**\n{data['html_url']}")
    else:
        print("Failed to fetch GitHub release info")

@tasks.loop(minutes=10)  # Check every 10 minutes
async def github_checker():
    await check_github_release()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    github_checker.start()

bot.run(TOKEN)
