# For testing src.linked_calendar functionalities.
from src.linked_calendar import LinkedCalendar
from src.calendar_image  import CalendarImage

def testCalendar() -> None:
  curr_month = 11

  cal = LinkedCalendar()
  cal.setCalendarIDByIndex(calendar_index=3)

  cal_image = CalendarImage()
  cal_image.initEmptyCalendarImage(month=curr_month)

  while True:
    user_input = input("ENTER TO UPDATE")
    if user_input == "exit":
      break

    removed_events, new_events = cal.getEventsForGivenMonth(month=curr_month)
    if (removed_events or new_events):
      print("Updating...")
    else:
      print(f"No new events for {curr_month}. :(")

    cal_image.updateCalendarImage(removed_events=removed_events,
                                  new_events=new_events)
    cal_image.saveCalendarImagePng()

testCalendar()
