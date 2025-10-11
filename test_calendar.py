# For testing src.linked_calendar functionalities.
from src.linked_calendar import LinkedCalendar

def testCalendar() -> None:

  cal = LinkedCalendar()
  cal.setCalendarIDByIndex(3)
  cal.updateEvents()
  print(f"All Events:\n{cal.getEventsStr(non_recurring=True)}")

testCalendar()
