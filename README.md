# Google Calendar Discord Bot
A Discord bot that posts updates on a given Google calendar so members of the server can keep up-to-date with events in said calendar.

## Capabilities and Details
### This bot can...
* connect to a specific, existing Google Calendar, and needs edit permissions.
* post weekly updates on the Google Calendar it's connected to in a specified channel.
  * These updates have a visual of the calendar for the current or following week, and can be set to post on a specific day out of the week.
* create channels in a specified server Category (e.g., 'Upcoming Events') for upcoming events.
  * These will be created automatically a set amount of days (up to user) before events in the bot's calendar.
  * Upon the channel's creation, it'll create a post with the title, date and time, and description of the event (all from the calendar event itself).
    * It will also have reaction messages for tracking attendance to the event.
      * **NOTE:** The attendance tracked in this post <ins>**will directly edit the calendar event attendence**</ins>, however this is the only time the bot will be editing anything on the calendar itself in order to prevent too much tampering with the calendar.
* post reminders for upcoming events in its calendar that have existing channels.
  * These will be posted in the same channel as the weekly updates.
* send DM reminders to those who don't affirm or decline attendance for an event before a certain amount of days before the event.
  * i.e., if the event is in (for example) 3 days, and someone hasn't yet marked whether or not they'll be attending, the bot can DM that individual with the event info and allows them to mark their attendence in that DM (rather than them having to go to the original message).
### It should be noted that...
* only those with a certain role (up to user) can edit the bots settings (like what updates/reminders to have on/off, the details on when those reminders should be, etc.).
* weekly updates/reminders the bot posts will @everyone by default, but this can be changed in settings.
* all the settings on the posts the bot makes (when the bot should post reminders, what updates/reminders should be on/off, where generated event channels should go, etc.) are configured by the user and can be adjusted at any time so the bot's automatic posts always conform to the user's specifications.

## Setup Instructions
* [click to add text]
