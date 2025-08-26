import discord
from discord.ui import Button

class AttendanceTracker(discord.ui.View):
  def __init__(self, *,
               confirmed: list[discord.Member],
               declined: list[discord.Member],
               non_respondents: list[discord.Member]):
    super().__init__()

    def attendance_stats_str():
      return (f"There are now {len(confirmed)} attending " +
              f"and {len(declined)} not attending, " +
              f"while {len(non_respondents)} have not yet responded.")

    # Button behaviors.
    async def yes_callback(interaction):
      user = interaction.user
      confirmed.append(user)
      try:
        non_respondents.remove(user)
      except ValueError:
        try:
          declined.remove(user)
        except ValueError:
          pass
      await interaction.response.send_message(attendance_stats_str())

    async def no_callback(interaction):
      user = interaction.user
      declined.append(user)
      try:
        non_respondents.remove(user)
      except ValueError:
        try:
          confirmed.remove(user)
        except ValueError:
          pass
      await interaction.response.send_message(attendance_stats_str())

    yes_btn = Button(emoji="✅")
    yes_btn.callback = yes_callback
    self.add_item(yes_btn)

    no_btn = Button(emoji="❌")
    no_btn.callback = no_callback
    self.add_item(no_btn)
