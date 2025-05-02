import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

print("Loading environment...")
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

print("TOKEN loaded:", "Yes" if TOKEN else "No")
print("CHANNEL_ID loaded:", CHANNEL_ID)

try:
    CHANNEL_ID = int(CHANNEL_ID)
except ValueError:
    print("Error: CHANNEL_ID must be an integer")
    exit()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("**AI HUB is now live! Use !picks or !mlbpicks to get today's bets.**")
    else:
        print("Channel not found. Check if bot is in the right server and has access.")

@bot.command()
async def picks(ctx):
    await ctx.send("**NBA AI Picks:**\n[0.85u] LeBron OVER 2.5 3PM — +115 at FanDuel (Proj: 3.3)")

@bot.command()
async def mlbpicks(ctx):
    await ctx.send("**MLB AI Picks:**\n[0.75u] Aaron Nola OVER 6.5 Ks — +100 at Caesars (Proj: 7.4)")

bot.run(TOKEN)
