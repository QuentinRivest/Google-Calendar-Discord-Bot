import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

import src.bot_settings
import src.event_post
import src.weekly_schedule_post

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Bot permissions.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

G_BOT_SETTINGS = src.bot_settings.BotSettings()

bot = commands.Bot(command_prefix='!', intents=intents)

# Prints message to terminal once bot is ready.
@bot.event
async def on_ready() -> None:
  print(f"Hello! {bot.user.name} reporting for duty. >:)")

@bot.event
async def on_guild_available(guild: discord.Guild) -> None:
  G_BOT_SETTINGS.server_guild = guild
  G_BOT_SETTINGS.target_role = guild.default_role

# Responds to user with certain role that use '!hi' command.
@bot.command()
@commands.has_role(G_BOT_SETTINGS.edit_perm_role_name)
async def hi(context: commands.Context) -> None:
  await context.send(f"Hello {context.author.mention}!")

# Posts weekly calendar.
@bot.command()
async def week(context: commands.Context) -> None:
  ex_img_filename = "chameleon.jpg"
  ex_img_file = discord.File("assets/chameleon.jpg", filename=ex_img_filename)
  ex_weekly = src.weekly_schedule_post.WeeklySchedulePost(ex_img_file)

  await context.send(file=ex_img_file,
                     embed=ex_weekly.weekly_embed,
                     view=ex_weekly.calendar_btn)

# Posts event post.
@bot.command()
async def post(context: commands.Context) -> None:
  event_msg: discord.Message
  ex_event = src.event_post.EventPost(G_BOT_SETTINGS)

  # Placeholder for setting up designated Events Category
  G_BOT_SETTINGS.events_category = G_BOT_SETTINGS.server_guild.categories[1]
  new_event_channel: discord.TextChannel = await G_BOT_SETTINGS.events_category.create_text_channel(name=ex_event.title)
  event_msg = await new_event_channel.send(embed=ex_event.event_embed, view=ex_event.attend_trkr_view)
  ex_event.setEventMsg(event_msg)
  await event_msg.pin()

bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)
