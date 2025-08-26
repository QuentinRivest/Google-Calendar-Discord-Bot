import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

from bot_settings import Settings

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Bot permissions.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot_settings = Settings()

bot = commands.Bot(command_prefix='!', intents=intents)

# Prints message to terminal once bot is ready.
@bot.event
async def on_ready():
  print(f"Hello! {bot.user.name} reporting for duty. >:)")

# Responds to user with certain role that use '!hi' command.
@bot.command()
@commands.has_role("everyone")
async def hi(context):
  await context.send(f"Hello {context.author.mention}!")

"""✅❌"""

class AttendanceButtons(discord.ui.View):
  def __init__(self):
    super().__init__()

    # Set up the post.
    self.add_item(discord.ui.Button(emoji="✅"))
    self.add_item(discord.ui.Button(emoji="❌"))

class EventPostInfo():
  def __init__(self):
    super().__init__()

    # TODO: Set event details from calendar.
    title = "Placeholder Event"
    description = "This is an example of a description for a placeholder event."
    # calendar_url = "https://calendar.google.com/calendar/u/0/r/week/2025/9/5?pli=1"

    self.event_info = discord.Embed(description=(title + "\n\n" + description), color=0x11AAAA)


ex_event = EventPostInfo()

# Creates an event post.
@bot.command()
async def post(context):
  await context.send(embed=ex_event.event_info, view=AttendanceButtons())

# Sends DM to a user, 'msg' being the message contents.
@bot.command()
async def dm(context, *, msg):
  await context.author.send()

bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)
