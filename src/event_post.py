import copy
import discord

from . import bot_settings

class EventPost():
  def __init__(self, bot_settings: bot_settings.BotSettings):
    super().__init__()

    # TODO: Set event details from calendar.
    self.title = "Placeholder Event"
    self.description = "This is an example of a description for a placeholder event."
    # calendar_url = "https://calendar.google.com/calendar/u/0/r/week/2025/9/5?pli=1"

    # Event info.
    self.event_embed = discord.Embed(title=self.title,
                                     description=self.description,
                                     color=0x11AAAA)

    # Attendee stats.
    self.confirmed_attendees = []
    self.declined_attendees  = []
    self.non_respondents = list(bot_settings.target_role.members)

    # Entire event post message (with info and attendance tracker).
    self.event_msg: discord.Message

    self.attendance_view = AttendanceTrackerView(
      confirmed=self.confirmed_attendees,
      declined=self.declined_attendees,
      non_respondents=self.non_respondents
    )

  def setEventMsg(self, msg: discord.Message) -> None:
    self.event_msg = msg
    self.attendance_view.setEventMsg(msg)



class AttendanceTrackerView(discord.ui.View):
  def __init__(self, *,
               confirmed: list[discord.Member],
               declined: list[discord.Member],
               non_respondents: list[discord.Member]):
    super().__init__()

    self.event_msg: discord.Message

    def getConfirmedListStr() -> str:
      list_str = ""
      for mbr in confirmed:
        list_str += (mbr.display_name + '\n')
      return list_str

    def getDeclinedListStr() -> str:
      list_str = ""
      for mbr in declined:
        list_str += (mbr.display_name + '\n')
      return list_str

    def getUpdatedEmbed() -> discord.Embed:
      event_embed_copy = copy.deepcopy(self.event_msg.embeds[0])
      event_embed_copy.clear_fields()
      event_embed_copy.add_field(name="Attending:",
                                 value=getConfirmedListStr(),
                                 inline=False)
      event_embed_copy.add_field(name="Not Attending:",
                                 value=getDeclinedListStr(),
                                 inline=False)
      event_embed_copy.add_field(name=f"{len(non_respondents)} members have not responded yet.",
                                 value="")
      return event_embed_copy

    # Button behaviors.
    async def yesCallback(interaction: discord.Interaction) -> None:
      user = interaction.user
      confirmed.append(user)
      try:
        non_respondents.remove(user)
      except ValueError:
        try:
          declined.remove(user)
        except ValueError:
          pass
      await interaction.response.edit_message(embed=getUpdatedEmbed())

    async def noCallback(interaction: discord.Interaction) -> None:
      user = interaction.user
      declined.append(user)
      try:
        non_respondents.remove(user)
      except ValueError:
        try:
          confirmed.remove(user)
        except ValueError:
          pass
      await interaction.response.edit_message(embed=getUpdatedEmbed())

    yes_btn = discord.ui.Button(emoji="✅")
    yes_btn.callback = yesCallback
    self.add_item(yes_btn)

    no_btn = discord.ui.Button(emoji="❌")
    no_btn.callback = noCallback
    self.add_item(no_btn)

  def setEventMsg(self, msg: discord.Message) -> None:
    self.event_msg = msg
