import discord

from . import bot_settings

# IN DEVELOPMENT
class SettingsModal(discord.ui.Modal, title="Bot Settings"):
  def __init__(self, bot_settings_obj: bot_settings.BotSettings):
    super().__init__()

  # ...
