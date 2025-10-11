# Should display all events of that week, even recurring.
# Display nonrecurring events in a different color than recurring events.
# (MAYBE) Put extra note at bottom if recurring event is missing from its usual
#   location.
  # IF this IS done, it would mean maintaining a list of recurring events,
  #   which would have to be updated accordingly
    # removing events form the list after the final recurring event
    # adding an event to the list where a new recurring event is found

import discord

from . import go_to_calendar_button

class MonthlyUpdatePost():
  def __init__(self, img_file: discord.File):
    # Title and image of week schedule.
    self.monthly_embed = discord.Embed(title="Week of This/Next Monday")
    self.monthly_embed.set_image(url=("attachment://" + img_file.filename))

    # Get calendar link of current week.
    YYYYMD_str   = "2025/10/31"
    ex_cal_url = "https://calendar.google.com/calendar/u/0/r/week/" + YYYYMD_str
    self.calendar_btn = go_to_calendar_button.GoToCalendarButton(ex_cal_url)
