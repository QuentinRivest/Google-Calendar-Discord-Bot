import discord

from . import go_to_calendar_button

class WeeklySchedulePost():
  def __init__(self, img_file: discord.File):
    super().__init__()

    # Title and image of week schedule.
    self.weekly_embed = discord.Embed(title="Week of This/Next Monday")
    self.weekly_embed.set_image(url=("attachment://" + img_file.filename))

    # Get calendar link of current week.
    ex_cal_url = "https://calendar.google.com/calendar/u/0/r/week/2025/9/5?pli=1"
    self.calendar_btn = go_to_calendar_button.GoToCalendarButton(ex_cal_url)
