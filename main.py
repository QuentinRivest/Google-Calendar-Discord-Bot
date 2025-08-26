import discord
from discord.ext import commands
from discord.ui import Button
import logging
from dotenv import load_dotenv
import os

import inc.bot_settings
import inc.event_post

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Bot permissions.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

global_bot_settings = inc.bot_settings.BotSettings()

bot = commands.Bot(command_prefix='!', intents=intents)

# Prints message to terminal once bot is ready.
@bot.event
async def on_ready():
  print(f"Hello! {bot.user.name} reporting for duty. >:)")

@bot.event
async def on_guild_available(guild: discord.Guild):
  global_bot_settings.server_guild = guild
  global_bot_settings.target_role = guild.default_role

# Responds to user with certain role that use '!hi' command.
@bot.command()
@commands.has_role(global_bot_settings.edit_perm_role_name)
async def hi(context):
  await context.send(f"Hello {context.author.mention}!")

# Posts event post.
@bot.command()
async def post(context):
  ex_event = inc.event_post.EventPost(global_bot_settings)
  await context.send(embed=ex_event.event_info, view=ex_event.attendance_tracker)


bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)
