import discord

from . import bot_settings
from . import attendance_tracker

class EventPost():
  def __init__(self, bot_settings: bot_settings.BotSettings):
    super().__init__()

    # TODO: Set event details from calendar.
    title = "Placeholder Event"
    description = "This is an example of a description for a placeholder event."
    # calendar_url = "https://calendar.google.com/calendar/u/0/r/week/2025/9/5?pli=1"

    # Event info.
    self.event_embed = discord.Embed(title=title, description=description, color=0x11AAAA)

    # Attendee stats.
    self.confirmed_attendees: list[discord.Member] = []
    self.declined_attendees: list[discord.Member] = []
    self.non_respondents = list(bot_settings.target_role.members)

    self.attendance_tracker = attendance_tracker.AttendanceTracker(
      confirmed=self.confirmed_attendees,
      declined=self.declined_attendees,
      non_respondents=self.non_respondents
    )
