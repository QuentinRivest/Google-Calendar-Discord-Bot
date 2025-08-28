import discord

class BotSettings:
  def __init__(self):
    # The discord.Guild object (the server) that the bot exists in.
    self.server_guild: discord.Guild
    # The role that is given permission to edit the bot settings.
    self.edit_perm_role_name = "@everyone"
    # The role that notifications will be targeted toward.
    self.target_role: discord.Role
    # The server Category that new event channels will be created in.
    self.events_category: discord.CategoryChannel
