# TODO: change the whole authentication part.
# 'Cause this code's for a desktop app, but it should be a webapp.
# Gotta set up a server er somethin' with Flask?
# And secure storing of user tokens, like with encryption'n all.

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

# This app only gets READONLY data from a user's calendar.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

class LinkedCalendar:
  # Object for interacting with Google Calendar API that all LinkedCalendar objs
  # can use.
  __api_service: Resource = None
  #
  __creds: Credentials = None

  def __init__(self):
    # The ID of the specific calendar chosen out of the list of calendars the
    # user has.
    self.calendar_id: str = "primary"
    self.events_list: list[dict] = []

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      LinkedCalendar.__creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
      )
    else:
      print("No token json file. :(")
    # If there are no (valid) credentials available, let the user log in.
    if not LinkedCalendar.__creds or not LinkedCalendar.__creds.valid:
      if LinkedCalendar.__creds and LinkedCalendar.__creds.expired and LinkedCalendar.__creds.refresh_token:
        LinkedCalendar.__creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        LinkedCalendar.__creds = flow.run_local_server(port=8080)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(LinkedCalendar.__creds.to_json())

    # Initialize service obj for interacting with the API.
    if not LinkedCalendar.__api_service:
      LinkedCalendar.__api_service = build("calendar",
                                           "v3",
                                           credentials=LinkedCalendar.__creds)

    # Set events_list to events of default "primary" calendar.
    self.updateEventsList()

  # Set the calendar ID for this instance.
  # (through command line rn, but will be set up through bot's settings)
  def setCalendarIdThruCmdLn(self) -> None:
    try:
      calendar_list_resp = LinkedCalendar.__api_service.calendarList().list().execute()
      calendar_list = calendar_list_resp.get("items")

      for i, calendar in enumerate(calendar_list):
        print(f"{i}: {calendar.get('summary')}")

      user_choice = input("Pick the number associated with the calendar you want: ")
      try:
        self.calendar_id = calendar_list[int(user_choice)].get("id")
      except ValueError as error:
        print(f"Issue retrieving calendar ID: {error}")
    except HttpError as error:
      print(f"An error occurred: {error}")

  def updateEventsList(self) -> None:
    now = getNowStr()

    try:
      events_resp = (
          LinkedCalendar.__api_service.events()
          .list(
              calendarId=self.calendar_id,
              timeMin=now,
              maxResults=10,
              singleEvents=True,
              orderBy="startTime",
          )
          .execute()
      )
    except HttpError as error:
      print(f"An error occurred: {error}")

    self.events_list = events_resp.get("items", [])

  def printEvents(self) -> None:
    if not self.events_list:
      print("No upcoming events found.")
      return

    # Prints the start and name of the next 10 events
    for event in self.events_list:
      start = event["start"].get("dateTime", event["start"].get("date"))
      print(start, event["summary"])



# HELPER FUNCTIONS
def getNowStr() -> str:
  return datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
