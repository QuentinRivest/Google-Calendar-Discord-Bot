# This is for testing out the generating for the graphic image that'll be used
#   to display the events for that month.
# Possible libraries to use for this:
  # Pillow (seems like you need to do more stuff manually for this one)
  # Matplotlib (handles as a canvas element, I think)

import matplotlib.pyplot as plt
from matplotlib.table import Table


## GLOBALS

# Table/Cell Dimensions Info
ROWS   = 7
COLS   = 7
WIDTH  = 1 / COLS
HEIGHT = 1 / ROWS

# Colors
TITLE_TEXT_COLOR         = "#cccccc"
BACKGROUND_COLOR         = "#1f1f1f"
EMPTY_CELL_COLOR         = "#555555"
RECURRING_EVENT_COLOR    = "#8877ff"
NONRECURRING_EVENT_COLOR = "#cca800"

# Text Formats
DAY_HEADER_TEXT_FORMAT = {
    'fontsize': 18,
    'color': TITLE_TEXT_COLOR,
    'horizontalalignment': 'center'
}
CELL_TEXT_FORMAT = {
    'fontsize': 10,
    'color': "#000000",
    'verticalalignment': 'bottom',
    'horizontalalignment': 'left'
}


# Create a figure and a single subplot (axes)
fig, ax = plt.subplots(figsize=(10, 7))
fig.set_facecolor(BACKGROUND_COLOR)
# fig.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98)
ax.axis("off")

table = Table(ax)
table.auto_set_font_size(False)

calendar = [[False, True, False, True, False, False, False],
            [False, True, False, True, False, True,  False],
            [False, True, False, True, False, False, False],
            [False, True, True,  True, False, False, True ],
            [False, True, False, True, False, False, True ],
            [False, True, False, True, False, False, False]]

days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

for c in range(COLS):
  cell = table.add_cell(
    row=0,
    col=c,
    width=WIDTH,
    height=0.09,
    text=days_of_week[c],
    facecolor=BACKGROUND_COLOR
  )
  cell.set_linewidth(0)
  cell.get_text().update(DAY_HEADER_TEXT_FORMAT)


for r in range(1, ROWS):
  for c in range(COLS):
    is_occupied = calendar[r-1][c]
    text = f"({r},{c})" if is_occupied else ""
    face_color = RECURRING_EVENT_COLOR if is_occupied else EMPTY_CELL_COLOR

    cell = table.add_cell(
      row=r,
      col=c,
      width=WIDTH,
      height=HEIGHT,
      text=text,
      facecolor=face_color
    )
    cell.set_edgecolor(BACKGROUND_COLOR)
    cell.set_linewidth(1)
    cell.get_text().update(CELL_TEXT_FORMAT)

ax.add_table(table)
curr_month = "October"
ax.set_title(label=curr_month, loc="left", fontsize=30, color=TITLE_TEXT_COLOR)

plt.savefig('cal.png', bbox_inches="tight", pad_inches=0.1)
plt.show()
