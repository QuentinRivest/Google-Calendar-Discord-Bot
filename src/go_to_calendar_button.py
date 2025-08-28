import discord
from discord.ui import Button

class GoToCalendarButton(discord.ui.View):
  def __init__(self, calendar_url: str):
    super().__init__()

    self.add_item(Button(label="Go to Calendar", url=calendar_url))
