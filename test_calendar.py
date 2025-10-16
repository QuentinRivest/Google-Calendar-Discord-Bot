# For testing src.linked_calendar functionalities.
from src.linked_calendar import LinkedCalendar
from src.calendar_image  import CalendarImage

def testCalendar() -> None:
  while True:
    try:
      curr_month = int(input("Enter valid month integer: "))
    except ValueError:
      continue

    if curr_month < 1 or 12 < curr_month: continue

    cal = LinkedCalendar()
    cal.setCalendarIDByIndex(calendar_index=3)
    cal.updateEventsForGivenMonth(month=curr_month)
    # print(f"All Events:\n{cal.getEventsStr(non_recurring=True)}")

    cal_image = CalendarImage()
    cal_image.createCalendarImage(month=curr_month, events_list=cal.getEventsList())
    cal_image.showCalendarImage()
    # cal_image.saveCalendarImagePng()

testCalendar()
