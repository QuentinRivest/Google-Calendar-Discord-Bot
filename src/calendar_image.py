# This is for testing out the generating for the graphic image that'll be used
#   to display the events for that month.
# Possible libraries to use for this:
  # Pillow (seems like you need to do more stuff manually for this one)
  # Matplotlib (handles as a canvas element, I think)

import matplotlib.pyplot as plt
from matplotlib.table import Table

from . import linked_calendar


class CalendarImage:
  # Table/Cell Dimensions Info
  __MAX_ROWS               = 7  # Could be 5-7 rows
  __COLS                   = 7
  __CELL_WIDTH             = 1 / __COLS
  __CELL_HEIGHT            = 1 / __MAX_ROWS
  __WEEK_LABEL_CELL_HEIGHT = 0.1

  # Labels
  __DAYS_OF_THE_WEEK = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

  # Colors
  __TITLE_TEXT_COLOR         = "#cccccc"
  __BACKGROUND_COLOR         = "#1f1f1f"
  __EMPTY_CELL_COLOR         = "#555555"
  __RECURRING_EVENT_COLOR    = "#8877ff"
  __NONRECURRING_EVENT_COLOR = "#cca800"

  # Text Formats
  __DAY_HEADER_TEXT_FORMAT = {
      "fontsize"            : 18,
      "color"               : __TITLE_TEXT_COLOR,
      "horizontalalignment" : "center"
  }
  # TODO: figure out how to format cell text.
  __CELL_TEXT_FORMAT = {
      "fontsize"            : 8,
      "color"               : "#000000",
      "verticalalignment"   : "top",
      "horizontalalignment" : "left"
  }
  __CELL_TEXT_PADDING = 0.1

  # Render Info
  __RENDER_WIDTH   = 10
  __RENDER_HEIGHT  = 7
  __PADDING_INCHES = 0.3


  def __init__(self):
    # Create a figure and a single subplot (axes)
    self.__figure, self.__axes = plt.subplots(
      figsize=(CalendarImage.__RENDER_WIDTH,
               CalendarImage.__RENDER_HEIGHT))
    self.__figure.set_facecolor(CalendarImage.__BACKGROUND_COLOR)
    self.__axes.axis("off")
    self.__calendar: Table

    self.__first_of_month_offset = 0  # valid values interval: [0, 6]


  # Updates the calendar image (i.e., self.__calendar)
  def updateSingleCalendarImageEvent(self, *, event: linked_calendar.Event):
    pass

  # TODO: support multiple events per day, as right now it would overwrite
    # Will probably need a data structure to keep track of the events currently
    #   listed in the CalendarImage table on a given day.
  # TODO:
  # Resets the calendar image (i.e., self.__calendar) according to given month
  # and list of events.
  def createCalendarImage(self,
                          *,
                          month: int,
                          events_list: list[linked_calendar.Event]) -> None:
    self.__calendar = Table(self.__axes)
    self.__calendar.auto_set_font_size(False)

    first_dt, last_dt = linked_calendar.getFirstAndLastDtOfGivenMonth(month)

    self.__first_of_month_offset = first_dt.weekday()

    current_month_str = first_dt.strftime("%B")

    # Set up first row with day-of-the-week labels.
    for c in range(CalendarImage.__COLS):
      cell = self.__calendar.add_cell(
        row=0,
        col=c,
        width=CalendarImage.__CELL_WIDTH,
        height=CalendarImage.__WEEK_LABEL_CELL_HEIGHT,
        text=CalendarImage.__DAYS_OF_THE_WEEK[c],
        facecolor=CalendarImage.__BACKGROUND_COLOR
      )
      cell.set_linewidth(0)
      cell.get_text().update(CalendarImage.__DAY_HEADER_TEXT_FORMAT)

    # Actual content of the calendar.
    events_list_ptr = 0
    for r in range(1, CalendarImage.__MAX_ROWS):
      reached_end_of_calendar = False
      first_col               = self.__first_of_month_offset if r == 1 else 0

      for c in range(first_col, CalendarImage.__COLS):
        day_at_rc = self.__getDayFromRowCol(r, c)

        if day_at_rc > last_dt.day:
          reached_end_of_calendar = True
          break

        event     = events_list[events_list_ptr] if events_list_ptr < len(events_list) else None
        event_dt  = event.start_dt               if not event is None                  else None

        if not event is None and day_at_rc == event_dt.day:
          text       = f"{day_at_rc}\n• {event.title}\n  @{event_dt.strftime('%I:%M %p')}!"
          cell_color = CalendarImage.__RECURRING_EVENT_COLOR
          events_list_ptr += 1
        else:
          text       = f"{day_at_rc}"
          cell_color = CalendarImage.__EMPTY_CELL_COLOR

        cell = self.__calendar.add_cell(
          row=r,
          col=c,
          width=CalendarImage.__CELL_WIDTH,
          height=CalendarImage.__CELL_HEIGHT,
          text=text,
          facecolor=cell_color
        )
        cell.set_edgecolor(CalendarImage.__BACKGROUND_COLOR)
        cell.set_linewidth(1)
        cell.get_text().update(CalendarImage.__CELL_TEXT_FORMAT)
        cell.PAD = CalendarImage.__CELL_TEXT_PADDING

      if reached_end_of_calendar: break

    self.__axes.add_table(self.__calendar)
    self.__axes.set_title(label=current_month_str,
                          loc="left",
                          fontsize=30,
                          color=CalendarImage.__TITLE_TEXT_COLOR)


  def saveCalendarImagePng(self):
    plt.savefig("./assets/cal.png", bbox_inches="tight",
                pad_inches=CalendarImage.__PADDING_INCHES)


  def showCalendarImage(self):
    plt.show()


  ## CLASS HELPERS

  def __getDayFromRowCol(self, row: int, col: int) -> int:
    # Subtracting 1 from 'row' to ignore the first row, which is for the day of
    #   the week labels.
    # Add 1 at the end since it start at 0 otherwise, not 1.
    return (row - 1) * 7 + col - self.__first_of_month_offset + 1

  def __getRowColFromDay(self, day: int) -> tuple[int, int]:
    day += (self.__first_of_month_offset - 1)
    col = day % 7
    row = day / 7 + 1
    return (row, col)

  ## END HELPERS
