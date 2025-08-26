import discord
from discord.ui import Button
import copy

class AttendanceTracker(discord.ui.View):
  def __init__(self, *,
               confirmed: list[discord.Member],
               declined: list[discord.Member],
               non_respondents: list[discord.Member]):
    super().__init__()

    self.event_msg: discord.Message

    def getConfirmedListStr() -> str:
      list_str: str = ""
      for mbr in confirmed:
        list_str += (mbr.display_name + '\n')
      return list_str

    def getDeclinedListStr() -> str:
      list_str: str = ""
      for mbr in declined:
        list_str += (mbr.display_name + '\n')
      return list_str

    def getUpdatedEmbed() -> discord.Embed:
      event_embed_copy: discord.Embed = copy.deepcopy(self.event_msg.embeds[0])
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
    async def yesCallback(interaction: discord.Interaction):
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

    async def noCallback(interaction):
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

    yes_btn = Button(emoji="✅")
    yes_btn.callback = yesCallback
    self.add_item(yes_btn)

    no_btn = Button(emoji="❌")
    no_btn.callback = noCallback
    self.add_item(no_btn)

  def setEventMsg(self, msg: discord.Message):
    self.event_msg = msg
