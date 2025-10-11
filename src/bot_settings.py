import discord

class BotSettings:
  def __init__(self):
    ### General Settings

    # The discord.Guild object (the server) that the bot exists in.
    self.server_guild: discord.Guild
    # The role that is given permission to edit the bot settings.
    self.edit_perm_role_name = "@everyone"

    # The Google Calendar the bot is connected to.
      # Not sure how this'd work... maybe it'd be a button that leads to the OAuth.
    # Which calendar to post events from.

    ### Event Post settings

    ## Event Post
    # Whether to do the event posts at all, which are automatic.
    self.do_event_posts: bool = True
    # The server Category that new event channels will be created in.
    self.events_category: discord.CategoryChannel
    # The number of days in advance to post an upcoming event.
    self.leadtime_for_event_post: int = 10
    # The role that event posts with @ mention will be targeted toward.
    self.events_notify_role: discord.Role

    ## Event Reminders
    # Whether to remind non-respondents.
    self.do_nonresp_reminder: bool = True
    # The role defining the subset of members to be reminded if not having responded.
    self.events_reminder_role: discord.Role
    # The number of days before the event non-respondents should be reminded.
    self.leadtime_for_nonresp_reminder: int = 5

    ### Google Calendar Regular Update Settings
    # Whether to do the regular updates in the first place.
    self.do_regular_cal_updates: bool = True
    # The text channel the updates should be posted in.
    self.cal_updates_channel: discord.TextChannel
    # Whether updates should be weekly, otherwise they'll be monthly.
    self.cal_updates_are_weekly: bool = True
    # The day of the week/month updates should occur.
    self.cal_updates_day: int = True  # Ranges: weekly=[1, 7], monthly=[1, 28]
    # The role that should be notified of these regular updates.
    self.cal_updates_role: discord.Role



# SETTINGS SELECTION OUTLINE; user decides...
  # [ROLE] role should have access to edit bot settings.
    # ASIDE: "[ROLE]" means it's a drop-down of server roles.
  # Would you like the bot to automatically post upcoming events? [Y/N]
    # Y:
      # Channels created for an event should be created in [CATEGORY].
      # Post events [INT] days before the event is to occur.
      # Notify [ROLE] role when event is posted.
      # Would you like the bot to notify those who haven't responded x days before the event? [Y/N]
        # Y:
          # Notify non-respondents with [ROLE] role [INT] days before the event.
  # Would you like the bot to post regular calendar updates? [Y/N]
    # Y:
      # Updates should be posted in [TEXT-CHANNEL].
      # Updates should be ["weekly"/"monthly"] every [DAY OF WEEK/MONTH] of the week/month ["prior to"/"of"].
      # Bot should notify [ROLE] role of calendar updates.
