import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
NBA_CHANNEL_ID = int(os.getenv("NBA_CHANNEL_ID", "0"))
MLB_CHANNEL_ID = int(os.getenv("MLB_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

eastern = pytz.timezone("US/Eastern")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    schedule_posts.start()

@bot.command()
async def picks(ctx):
    await ctx.send("**NBA AI Picks:**\n[0.85u] LeBron OVER 2.5 3PM — +115 at FanDuel (Proj: 3.3)")

@bot.command()
async def mlbpicks(ctx):
    await ctx.send("**MLB AI Picks:**\n[0.75u] Aaron Nola OVER 6.5 Ks — +100 at Caesars (Proj: 7.4)")

@tasks.loop(minutes=10)
async def schedule_posts():
    now = datetime.now(eastern)

    # Mock NBA game at 7 PM ET, post at 5 PM ET
    post_time_nba = eastern.localize(datetime(now.year, now.month, now.day, 17, 0))
    if now >= post_time_nba and now < post_time_nba + timedelta(minutes=10):
        channel = bot.get_channel(NBA_CHANNEL_ID)
        if channel:
            await channel.send("**NBA AI Picks:**\n[0.85u] LeBron OVER 2.5 3PM — +115 at FanDuel (Proj: 3.3)")

    # Mock MLB game at 7:10 PM ET, post at 5:10 PM ET
    post_time_mlb = eastern.localize(datetime(now.year, now.month, now.day, 17, 10))
    if now >= post_time_mlb and now < post_time_mlb + timedelta(minutes=10):
        channel = bot.get_channel(MLB_CHANNEL_ID)
        if channel:
            await channel.send("**MLB AI Picks:**\n[0.75u] Aaron Nola OVER 6.5 Ks — +100 at Caesars (Proj: 7.4)")

bot.run(TOKEN)
