# Just using the Google Calendar Python Quickstart code for now to get the
# functionality working the way I want it with the Discord bot portion.
# Then I'll redo it since this code is really just for Installed Apps, and I
# need it to work for Web Apps (since that's what this is, if I want it
# accessible to others, lol).

# TO-DO FOR WEB HOSTING FUNCTIONALITY
  # use a database (maybe using Flask, I think??) to store token/credential info
  #   for potentially multiple users
    # would need to use it with Google OAuth stuff, not just a username-pwd
    #   set up
    # encrypt info, I think... somehow
  # figure out how to use PythonAnywhere and put it on there

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import os.path

from google.auth.exceptions         import MutualTLSChannelError
from google.auth.transport.requests import Request
from google.oauth2.credentials      import Credentials
from google_auth_oauthlib.flow      import InstalledAppFlow
from googleapiclient.discovery      import build, Resource
from googleapiclient.errors         import HttpError


class LinkedCalendar:
  def __init__(self) -> None:
    # The ID of the specific calendar chosen out of the list of calendars the
    # user has.
    self.__calendar_id:         str              = "primary"
    self.__events:              dict[str, Event] = {}  # (id : event_obj)
    self.__recurring_event_IDs: set[str]         = set()


  # Print calendar labels ("summaries") and corresponding indices.
  def printCalendarListByIndex(self) -> None:
    api = self.__getServiceObject()

    try:
      calendar_list = api.calendarList().list().execute().get("items")

      for i, calendar in enumerate(calendar_list):
        print(f"{i}: {calendar.get('summary')}")

    except HttpError as error:
      print(f"ERROR: Issue getting calendar list: {error}")


  def setCalendarIDByIndex(self, *, calendar_index: int) -> None:
    api = self.__getServiceObject()

    try:
      calendar_list      = api.calendarList().list().execute().get("items")
      self.__calendar_id = calendar_list[int(calendar_index)].get("id")

    except HttpError as error:
      print(f"ERROR: Issue getting calendar list: {error}")
    except IndexError as error:
      print (f"ERROR: (probably) invalid calendar index given: {error}")

  # Returns bool for True if events were updated, False if not buuutt...
  #   I'd also want the actual events that were updated (changed/added/deleted),
  #   so the return type could be...
    # (1) tuple[list, list]
      # where the first list is the list of changed/added events, and the second
      #   is the list of deleted events
    # (2) tuple[list, list, list]
      # similar to (1), but a separate list for changed, added, and deleted
      # might be necessary if change and add operations are very different
      #   (which they might be, depending on the CalendarImage structure)
  def updateEventsForGivenMonth(self, *, month: int) -> bool:
    change_was_made_to_events = False

    api = self.__getServiceObject()

    # Set up for getting a whole month of events for the current year:
    time_min, time_max = getFirstAndLastDtOfGivenMonth(month)
    try:
      # Call the Calendar API
      retrieved_events: list[dict] = (
          api.events()
          .list(
              calendarId=self.__calendar_id,
              timeMin=time_min.isoformat(),
              timeMax=time_max.isoformat(),
              maxResults=100,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute().get("items", [])
      )

      retrieved_event_IDs = set()

      # Add events which are not recurring to obj's 'self.__events_list'.
      for event in retrieved_events:
        event_id   = event["id"]
        event_etag = event["etag"]
        retrieved_event_IDs.add(event_id)

        # Skip events that haven't changed.
        if event_id in self.__events and event_etag == self.__events[event_id].last_etag:
          continue

        change_was_made_to_events = True

        event_start_info = event["start"]
        start_dt_iso     = None
        end_dt_str       = None
        if "dateTime" in event_start_info:
          start_dt_iso = event_start_info["dateTime"]

          event_end_time_info = event["end"]
          if "dateTime" in event_end_time_info:
            end_dt_str = event_end_time_info["dateTime"]
        elif "date" in event_start_info:
          start_dt_iso = event_start_info["date"]


        event_obj = Event(
          id=event_id,
          last_etag=event_etag,
          url=event.get("htmlLink"),
          title=event.get("summary"),
          description=event.get("description"),
          start_dt_iso=start_dt_iso,
          end_dt_iso=end_dt_str
        )

        self.__events[event_id] = event_obj

        if "recurrence" in event or "recurringEventId" in event:
          self.__recurring_event_IDs.add(event_id)
    except HttpError as error:
      print(f"ERROR: Issue updating events list: {error}")

    # Remove events that are no longer in Google Calendar.
    old_events_count = len(self.__events)
    for event_id in self.__events:
      if not event_id in retrieved_event_IDs:
        del self.__events[event_id]

    return len(self.__events) < old_events_count or change_was_made_to_events


  def getEventsList(self):
    return list(self.__events.values())


  # For testing, lol.
  def getEventsStr(self, *, non_recurring: bool = False) -> str:
    events_list_str = ""

    for id, event in self.__events.items():
      if non_recurring and id in self.__recurring_event_IDs:
        continue

      default_str = "(Idk)"

      start            = event.start_dt
      event_date       = start.strftime("%b %d")    if not start is None else default_str
      event_start_time = start.strftime("%I:%M %p") if not start is None else default_str

      end            = event.end_dt
      event_end_time = end.strftime("%I:%M %p") if not end is None else default_str

      event_str = f"""{event.title} (ID: {id}):
      Description: {event.description}
      When: {event_date}, from {event_start_time} to {event_end_time}
      Link: {event.url}

"""

      events_list_str += event_str

    return events_list_str


  ## PRIVATE HELPERS

  def __getServiceObject(self) -> Resource:
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds: Credentials = None

    # The file ./auth/token.json stores the user's access and refresh tokens,
    # and is created automatically when the authorization flow completes for the
    # first time.
    if os.path.exists("./auth/token.json"):
      creds = Credentials.from_authorized_user_file("./auth/token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "./auth/credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open("./auth/token.json", "w") as token:
        token.write(creds.to_json())

    try:
      return build("calendar", "v3", credentials=creds)
    except MutualTLSChannelError as error:
      print(f"ERROR: issue setting up mutual TLS channel when building service object: {error}")



class Event:

  def __init__(
    self,
    *,
    id: str,
    last_etag: str,
    url: str,
    title: str,
    description: str,
    start_dt_iso: str,
    end_dt_iso: str
  ) -> None:
    self.id          = id
    self.last_etag   = last_etag
    self.url         = url
    self.title       = title
    self.description = description
    self.start_dt    = datetime.fromisoformat(start_dt_iso) if not start_dt_iso is None else None
    self.end_dt      = datetime.fromisoformat(end_dt_iso)   if not end_dt_iso   is None else None



## HELPERS

def getNowStr() -> str:
  return datetime.now(timezone.utc).isoformat()


def getDtInGivenDaysStr(days_count: int) -> str:
  return (datetime.now(timezone.utc) + timedelta(days=days_count)).isoformat()


def getFirstAndLastDtOfGivenMonth(current_month: int) -> tuple[datetime, datetime]:
  current_year = datetime.today().year

  pst = ZoneInfo("America/Los_Angeles")

  first_dt = datetime(year=current_year, month=current_month, day=1, tzinfo=pst)

  if (current_month == 1 or current_month == 3 or current_month == 5 or
      current_month == 7 or current_month == 8 or current_month == 10 or
      current_month == 12):
    last_day = 31
  elif (current_month == 4 or current_month == 6 or
        current_month == 9 or current_month == 11):
    last_day = 30
  else:  # is February
    if (current_year % 4 == 0 and current_year % 100 != 0 or
        current_year % 400 == 0):  # is leap year
      last_day = 29
    else:
      last_day = 28

  last_dt = first_dt.replace(day=last_day,
                             hour=23, minute=59, second=59)

  return (first_dt, last_dt)

## END HELPERS
