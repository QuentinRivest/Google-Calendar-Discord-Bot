import discord
import logging
import os
from discord.ext import commands
from dotenv      import load_dotenv

from src.bot_settings    import BotSettings
from src.event_post      import EventPost
from src.linked_calendar import LinkedCalendar
from monthly_update_post import MonthlyUpdatePost
from src.settings_modal  import SettingsModal

def botCommands():
  load_dotenv()
  discord_token = os.getenv('DISCORD_TOKEN')

  handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

  # Bot permissions.
  intents = discord.Intents.default()
  intents.message_content = True
  intents.members = True

  G_BOT_SETTINGS = BotSettings()

  bot = commands.Bot(command_prefix='!', intents=intents)

  # Prints message to terminal once bot is ready.
  @bot.event
  async def on_ready() -> None:
    print(f"Hello! {bot.user.name} reporting for duty. >:)")

  @bot.event
  async def on_guild_available(guild: discord.Guild) -> None:
    G_BOT_SETTINGS.server_guild = guild
    G_BOT_SETTINGS.target_role  = guild.default_role

  # Responds to user with certain role that use '!hi' command.
  @bot.command()
  @commands.has_role(G_BOT_SETTINGS.edit_perm_role_name)
  async def hi(context: commands.Context) -> None:
    await context.send(f"Hello {context.author.mention}!")

  # Posts weekly calendar.
  @bot.command()
  async def update(context: commands.Context) -> None:
    ex_img_filename = "chameleon.jpg"
    ex_img_file     = discord.File("assets/chameleon.jpg", filename=ex_img_filename)
    ex_weekly       = MonthlyUpdatePost(ex_img_file)

    await context.send(file=ex_img_file,
                       embed=ex_weekly.weekly_embed,
                       view=ex_weekly.calendar_btn)

  # Posts event post.
  @bot.command()
  async def post(context: commands.Context) -> None:
    ex_event = EventPost(G_BOT_SETTINGS)

    # Placeholder for setting up designated Events Category
    G_BOT_SETTINGS.events_category = G_BOT_SETTINGS.server_guild.categories[1]

    new_event_channel = await G_BOT_SETTINGS.events_category.create_text_channel(
      name=ex_event.title)

    event_msg = await new_event_channel.send(
      embed=ex_event.event_embed, view=ex_event.attendance_view)
    ex_event.setEventMsg(event_msg)
    await event_msg.pin()

  # Access bot settings
  @bot.command()
  async def settings(context: commands.Context) -> None:
    modal = SettingsModal(G_BOT_SETTINGS)

  # Post weekly
  @bot.command()
  async def weekly(context: commands.Context) -> None:
    cal = LinkedCalendar()
    cal.setCalendarIDByIndex(3)
    cal.updateEvents()
    await context.send(content=cal.getEventsStr(non_recurring=True))

  bot.run(discord_token, log_handler=handler, log_level=logging.DEBUG)

botCommands()
