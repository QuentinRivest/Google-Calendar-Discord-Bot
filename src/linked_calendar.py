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


  def setCalendarIDByIndex(self, calendar_index: int) -> None:
    api = self.__getServiceObject()

    try:
      calendar_list      = api.calendarList().list().execute().get("items")
      self.__calendar_id = calendar_list[int(calendar_index)].get("id")

    except HttpError as error:
      print(f"ERROR: Issue getting calendar list: {error}")
    except IndexError as error:
      print (f"ERROR: (probably) invalid calendar index given: {error}")


  # TODO: make sure that
  def updateEvents(self) -> None:
    api = self.__getServiceObject()

    try:
      # Call the Calendar API
      all_events: list[dict] = (
          api.events()
          .list(
              calendarId=self.__calendar_id,
              timeMin=getNowStr(),
              timeMax=getDtInGivenDaysStr(days_count=100),
              maxResults=100,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute().get("items", [])
      )

      # Add events which are not recurring to obj's 'self.__events_list'.
      for event in all_events:
        event_id   = event["id"]
        event_etag = event["etag"]

        if event_id in self.__events and event_etag == self.__events[event_id].last_etag:
          continue

        event_start_info = event["start"]
        start_dt_iso     = None
        end_dt_str     = None
        if "datetime" in event_start_info:
          start_dt_iso = event_start_info["datetime"]

          event_end_time_info = event["end"]
          if "datetime" in event_end_time_info:
            end_dt_str = event_end_time_info["datetime"][11:16]
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


  # For testing, lol.
  def getEventsStr(self, *, non_recurring: bool = False) -> str:
    events_list_str = ""

    for id, event in self.__events.items():
      if non_recurring and id in self.__recurring_event_IDs:
        continue

      event_str = f"""{event.title} (ID: {id}):
      Description: {event.description}
      When: {event.date_str_MonDYYYY} from {event.start_time_str} to {event.end_time_str}
      Link: {event.url}

"""

      events_list_str += event_str

    return events_list_str


  ## PRIVATE HELPERS

  def __getServiceObject(self) -> Resource:
    SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds: Credentials = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
      return build("calendar", "v3", credentials=creds)
    except MutualTLSChannelError as error:
      print(f"ERROR: issue setting up mutual TLS channel when building service object: {error}")



class Event:
  month_abbr_str = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

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
    self.id               = id
    self.last_etag        = last_etag
    self.url              = url
    self.title            = title
    self.description      = description
    self.start_dt_str_iso = start_dt_iso

    self.date_str_MMDDYYYY = None
    self.date_str_MonDYYYY = None
    self.start_time_str    = None
    self.end_time_str      = None

    if not start_dt_iso is None:
      yyyy = start_dt_iso[:4]
      m    = start_dt_iso[5:7]
      d    = start_dt_iso[8:10]
      self.date_str_MMDDYYYY = m + "/" + d + "/" + yyyy

      mon_str = Event.month_abbr_str[int(m) - 1]
      day_str = d[1] if d[0] == "0" else d
      self.date_str_MonDYYYY = mon_str + " " + day_str + ", " + yyyy

      if len(start_dt_iso) > 15:  # start_dt_iso has a time component
        self.start_time_str = get24hrTo12hr(start_dt_iso[11:16])
        self.end_time_str   = get24hrTo12hr(end_dt_iso[11:16])



## HELPERS

def getNowStr() -> str:
  return datetime.now(timezone.utc).isoformat()


def getDtInGivenDaysStr(days_count: int) -> str:
  return (datetime.now(timezone.utc) + timedelta(days=days_count)).isoformat()


def getFirstAndLastOfCurrentMonth() -> tuple[str, str]:
  now = datetime.now(timezone=ZoneInfo("AmericAmerica/Los_Angeles"))

  first_dt = now
  first_dt.day = 1

  current_month = now.month
  if (current_month == 1 or current_month == 3 or current_month == 5 or
      current_month == 7 or current_month == 8 or current_month == 10 or
      current_month == 12):
    last_day = 31
  elif (current_month == 4 or current_month == 6 or
        current_month == 9 or current_month == 11):
    last_day = 30
  else:  # is February
    current_year = now.year
    if (current_year % 4 == 0 and current_year % 100 != 0 or
        current_year % 400 == 0):  # is leap year
      last_day = 29
    else:
      last_day = 28

  last_dt = now
  last_dt.day = last_day

  return (first_dt, last_dt)



def get24hrTo12hr(time24: str) -> str:  # of format HH:MM
  hr24, min = time24[:2], time24[3:]
  suffix = "am"

  hr12 = hr24
  if hr24 == "00":
    hr12 = "12"
  elif int(hr24) > 11:
    offset = 0 if hr24 == 12 else 12
    hr12   = str(int(hr24) - offset)
    suffix = "pm"

  return hr12 + ":" + min + suffix
