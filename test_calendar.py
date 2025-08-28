from src.linked_calendar import LinkedCalendar

def testCalendar() -> None:
  cal = LinkedCalendar()
  cal.setCalendarIdThruCmdLn()
  cal.updateEventsList()
  cal.printEvents()

testCalendar()
