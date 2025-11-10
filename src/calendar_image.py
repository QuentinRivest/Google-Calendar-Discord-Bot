# This is for testing out the generating for the graphic image that'll be used
#   to display the events for that month.
# Possible libraries to use for this:
  # Pillow (seems like you need to do more stuff manually for this one)
  # Matplotlib (handles as a canvas element, I think)

from datetime import time

import matplotlib.pyplot as plt
from matplotlib.table   import Table
from matplotlib.patches import Rectangle

from . import linked_calendar


class CalendarImage:
  # Table/Cell Dimensions Info
  __COLS                   = 7
  # Rows may change, calculated from the number of cells each day.
  __CELLS_PER_DAY_DEFAULT  = 4
  __CELL_WIDTH             = 0.143
  __CELL_HEIGHT            = 0.047
  __DAY_LABEL_CELL_HEIGHT  = 0.03
  __WEEK_LABEL_CELL_HEIGHT = 0.1

  # Render Info
  __RENDER_WIDTH      = 10
  __PADDING_INCHES    = 0.3

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
      "verticalalignment"   : "top",
      "horizontalalignment" : "center"
  }
  __CELL_TEXT_FORMAT = {
      "fontsize"            : 8,
      "color"               : "#000000",
      "verticalalignment"   : "center",
      "horizontalalignment" : "left"
  }


  def __init__(self):
    # Create a figure and a single subplot (axes)
    self.__figure, self.__axes = plt.subplots()
    self.__figure.set_facecolor(CalendarImage.__BACKGROUND_COLOR)
    self.__axes.axis("off")

    self.__cells_per_day = CalendarImage.__CELLS_PER_DAY_DEFAULT

    self.__first_of_month_offset = 0  # valid values interval: [0, 6]

    # Can take [row, col] tuple to get the Cell at that location in the Table.
    self.__calendar: Table

    self.__cell_coord_to_event_ID: dict[tuple[int, int], str] = {}
    self.__event_ID_to_cell_coord: dict[str, tuple[int, int]] = {}
    self.__event_ID_to_event_time: dict[str, time]            = {}


  # Updates the calendar image based on the events that have been removed or
  # added. Updated events will be removed and re-added.
  def updateCalendarImage(self,
                          *,
                          removed_events: list[linked_calendar.Event]=[],
                          new_events:     list[linked_calendar.Event]=[]):

    # TODO: FIX ISSUE W/ REMOVING EVENTS
      # When middle of three events is removed, the event below it is not
      #   getting shifted up like it's supposed to -- a gap remains. :/
      # IT'S THE SWAP FUNCTION. :(

    for event in removed_events:
      event_coord       = self.__event_ID_to_cell_coord[event.id]
      day_rows, day_col = self.__getCoordsFromDay(event.start_dt.day)

      self.__clearCell(event_coord)

      # Shift that empty cell below all non-empty cells under it.
      for row in range(event_coord[0] + 1, day_rows[-1] + 1):
        if not (row, day_col) in self.__cell_coord_to_event_ID:
          break
        self.__swapCells(event_coord, (row, day_col))
        event_coord = (row, day_col)

    for event in new_events:
      new_event_coord   = None
      day_rows, day_col = self.__getCoordsFromDay(event.start_dt.day)

      for row in day_rows:
        if self.__calendar[row, day_col].get_text().get_text() == "":
          new_event_coord = (row, day_col)
          break

      new_event_time                                 = event.start_dt.time()
      self.__cell_coord_to_event_ID[new_event_coord] = event.id
      self.__event_ID_to_cell_coord[event.id]        = new_event_coord
      self.__event_ID_to_event_time[event.id]        = new_event_time

      event_cell = self.__calendar[new_event_coord]
      event_cell.get_text().set_text(
        f"• {event.title}\n  @{event.start_dt.strftime('%I:%M %p')}"
      )
      event_cell.set_facecolor(
        CalendarImage.__RECURRING_EVENT_COLOR if event.is_recurring
        else CalendarImage.__NONRECURRING_EVENT_COLOR
      )

      # Shift new event up as needed to maintain time order.
      for row in range(new_event_coord[0] - 1, day_rows[0] - 1, -1):
        curr_cell_event_ID = self.__cell_coord_to_event_ID.get((row, day_col), "DNE")
        if curr_cell_event_ID == "DNE":
          break

        time_of_curr_cell = self.__event_ID_to_event_time[curr_cell_event_ID]

        # Stop once the updated event is in the right order.
        if new_event_time >= time_of_curr_cell:
          break

        self.__swapCells(new_event_coord, (row, day_col))
        new_event_coord = (row, day_col)



  # Resets the calendar image (i.e., self.__calendar) according to given month
  # with accurate day placement and numeric labels, but no events.
  def initEmptyCalendarImage(self, *, month: int) -> None:
    self.__calendar = Table(self.__axes)
    self.__calendar.auto_set_font_size(False)

    first_dt, last_dt = linked_calendar.getFirstAndLastDtOfGivenMonth(month)

    self.__first_of_month_offset = first_dt.weekday()

    # Set up first row with day-of-the-week labels.
    for col in range(CalendarImage.__COLS):
      cell = self.__calendar.add_cell(
        row=0,
        col=col,
        width=CalendarImage.__CELL_WIDTH,
        height=CalendarImage.__WEEK_LABEL_CELL_HEIGHT,
        fill=False,
        text=CalendarImage.__DAYS_OF_THE_WEEK[col]
      )
      cell.visible_edges = "open"
      cell.get_text().update(CalendarImage.__DAY_HEADER_TEXT_FORMAT)

    # Actual content of the calendar.
    for row in range(1, self.__getMaxRows()):
      reached_end_of_calendar = False
      first_col               = (
        self.__first_of_month_offset if row <= self.__cells_per_day
        else 0
      )

      for col in range(first_col, CalendarImage.__COLS):
        day_at_rc = self.__getDayFromCell(row, col)

        if day_at_rc > last_dt.day:
          reached_end_of_calendar = True
          break

        cell_number = row % self.__cells_per_day
        text        = str(day_at_rc) if cell_number == 1 else ""

        cell = self.__calendar.add_cell(
          row=row,
          col=col,
          width=CalendarImage.__CELL_WIDTH,
          height=(CalendarImage.__DAY_LABEL_CELL_HEIGHT if cell_number == 1
                  else CalendarImage.__CELL_HEIGHT),
          edgecolor=CalendarImage.__EMPTY_CELL_COLOR,
          facecolor=CalendarImage.__EMPTY_CELL_COLOR,
          text=text
        )
        cell.get_text().update(CalendarImage.__CELL_TEXT_FORMAT)
        cell.PAD = 0.04

    current_month_str = first_dt.strftime("%B")

    self.__axes.add_table(self.__calendar)
    self.__axes.set_title(label=current_month_str,
                          loc="left",
                          fontsize=30,
                          color=CalendarImage.__TITLE_TEXT_COLOR,
                          y=0.97)

    # This draw call to render the figure is necessary so that the xy position
    # of a table cell can be accessed when adding visible border edges.
    self.__figure.canvas.draw()

    # Add visible border edges to calendar days.
    for row in range(self.__cells_per_day,
                     self.__getMaxRows(),
                     self.__cells_per_day):
      reached_end_of_calendar = False
      first_col               = (
        self.__first_of_month_offset if row <= self.__cells_per_day
        else 0
      )

      for col in range(first_col, CalendarImage.__COLS):
        if self.__getDayFromCell(row, col) > last_dt.day:
          reached_end_of_calendar = True
          break


        # Add border to each group of cells to form day.
        xy = self.__calendar[row, col].get_xy()
        self.__axes.add_patch(
          Rectangle(xy=xy,
                    width=CalendarImage.__CELL_WIDTH,
                    height=CalendarImage.__DAY_LABEL_CELL_HEIGHT + CalendarImage.__CELL_HEIGHT * (self.__cells_per_day - 1),
                    edgecolor=CalendarImage.__BACKGROUND_COLOR,
                    fill=False,
                    linewidth=1)
          )

      if reached_end_of_calendar: break


  def saveCalendarImagePng(self):
    self.__figure.set_figwidth(CalendarImage.__RENDER_WIDTH)
    # Reset render height according to the final number of rows.
    self.__figure.set_figheight(self.__getMaxRows() * 0.35)
    plt.savefig("./assets/cal.png",
                bbox_inches="tight",
                pad_inches=CalendarImage.__PADDING_INCHES)


  def showCalendarImage(self):
    plt.show()


  ## CLASS HELPERS

  # Returns the max number of rows that should be in the underlying Table object
  # that represents the calendar.
  def __getMaxRows(self) -> int:
    return 6 * self.__cells_per_day + 1


  # Converts an event cell position (row-col coordinate) to the corresponding
  # day that that event cell is on.
  def __getDayFromCell(self, row: int, col: int) -> int:
    return (row - 1) // self.__cells_per_day * 7 + col - self.__first_of_month_offset + 1


  # Returns all event cell positions (row-col coordinates) on a given day (minus
  # the first cell that holds the dya number label) in the format:
  #   (row1, row2, ..., rowN, col)
  # where the total length of the return tuple is equal to self.__cells_per_day.
  def __getCoordsFromDay(self, day: int) -> tuple[list[int], int]:
    day += (self.__first_of_month_offset)
    col = day % 7 - 1
    row = (day // 7) * self.__cells_per_day + 1

    # Exclude row + 0, as that's the day number label.
    rows = [row + i for i in range(1, self.__cells_per_day)]
    return (rows, col)


  # Clears the given cell.
  def __clearCell(self, cell_coord: tuple[int, int]) -> None:
    cell = self.__calendar[cell_coord]
    cell.get_text().set_text("")
    cell.set_facecolor(CalendarImage.__EMPTY_CELL_COLOR)

    event_ID = self.__cell_coord_to_event_ID.pop(cell_coord)
    del self.__event_ID_to_cell_coord[event_ID]
    del self.__event_ID_to_event_time[event_ID]


  # Swaps the contents of two cells.
  def __swapCells(self,
                  cell1_coord: tuple[int, int],
                  cell2_coord: tuple[int, int]) -> None:
    if (not cell1_coord in self.__cell_coord_to_event_ID and
        not cell2_coord in self.__cell_coord_to_event_ID):
      return

    cell1 = self.__calendar[cell1_coord]
    cell2 = self.__calendar[cell2_coord]

    cell1_text      = cell1.get_text().get_text()
    cell1_facecolor = cell1.get_facecolor()

    cell1.get_text().set_text(cell2.get_text().get_text())
    cell1.set_facecolor(cell2.get_facecolor())

    cell2.get_text().set_text(cell1_text)
    cell2.set_facecolor(cell1_facecolor)

    # Update {coordinate : event_ID) and (event_ID : coordinate) pairs.
    if cell1_coord in self.__cell_coord_to_event_ID:  # cell1 was occupied cell before swap.
      old_cell1_event_ID = self.__cell_coord_to_event_ID[cell1_coord]
      old_cell2_event_ID = self.__cell_coord_to_event_ID.get(cell2_coord, "DNE")

      self.__cell_coord_to_event_ID[cell2_coord]        = old_cell1_event_ID
      self.__event_ID_to_cell_coord[old_cell1_event_ID] = cell2_coord

      if old_cell2_event_ID == "DNE":
        del self.__cell_coord_to_event_ID[cell1_coord]
      else:
        self.__cell_coord_to_event_ID[cell1_coord]        = old_cell2_event_ID
        self.__event_ID_to_cell_coord[old_cell2_event_ID] = cell1_coord
    else:  # Old cell1 was empty cell.
      old_cell2_event_ID = self.__cell_coord_to_event_ID[cell2_coord]

      self.__cell_coord_to_event_ID[cell1_coord]        = old_cell2_event_ID
      self.__event_ID_to_cell_coord[old_cell2_event_ID] = cell1_coord
      del self.__cell_coord_to_event_ID[cell2_coord]

  ## END HELPERS
