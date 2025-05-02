import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pytz
import gspread
from google.oauth2.service_account import Credentials

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
NBA_CHANNEL_ID = int(os.getenv("NBA_CHANNEL_ID", "0"))
MLB_CHANNEL_ID = int(os.getenv("MLB_CHANNEL_ID", "0"))
SHEET_NAME = "AI HUB Picks Log"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
eastern = pytz.timezone("US/Eastern")

# Setup Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME)
nba_tab = sheet.worksheet("NBA")
mlb_tab = sheet.worksheet("MLB")

def log_pick(tab, data):
    now = datetime.now(eastern).strftime("%Y-%m-%d")
    row = [now] + data
    tab.append_row(row)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    schedule_posts.start()

@bot.command()
async def picks(ctx):
    data = ["Kawhi Leonard", "Over 2.5 3PM", "2.5", "+115", "FanDuel", "3.3", "0.85", "High", "TBD"]
    await ctx.send("**NBA AI Picks:**\n[0.85u] Kawhi Leonard OVER 2.5 3PM — +115 at FanDuel (Proj: 3.3)")
    log_pick(nba_tab, data)

@bot.command()
async def mlbpicks(ctx):
    data = ["Aaron Nola", "Over 6.5 Ks", "6.5", "+100", "Caesars", "7.4", "0.75", "High", "TBD"]
    await ctx.send("**MLB AI Picks:**\n[0.75u] Aaron Nola OVER 6.5 Ks — +100 at Caesars (Proj: 7.4)")
    log_pick(mlb_tab, data)

@tasks.loop(minutes=10)
async def schedule_posts():
    now = datetime.now(eastern)
    post_time_nba = eastern.localize(datetime(now.year, now.month, now.day, 17, 0))
    post_time_mlb = eastern.localize(datetime(now.year, now.month, now.day, 17, 10))

    if post_time_nba <= now < post_time_nba + timedelta(minutes=10):
        channel = bot.get_channel(NBA_CHANNEL_ID)
        if channel:
            await channel.send("**NBA AI Picks:**\n[0.85u] Kawhi Leonard OVER 2.5 3PM — +115 at FanDuel (Proj: 3.3)")
            log_pick(nba_tab, ["Kawhi Leonard", "Over 2.5 3PM", "2.5", "+115", "FanDuel", "3.3", "0.85", "High", "TBD"])

    if post_time_mlb <= now < post_time_mlb + timedelta(minutes=10):
        channel = bot.get_channel(MLB_CHANNEL_ID)
        if channel:
            await channel.send("**MLB AI Picks:**\n[0.75u] Aaron Nola OVER 6.5 Ks — +100 at Caesars (Proj: 7.4)")
            log_pick(mlb_tab, ["Aaron Nola", "Over 6.5 Ks", "6.5", "+100", "Caesars", "7.4", "0.75", "High", "TBD"])

bot.run(TOKEN)
