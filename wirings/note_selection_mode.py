from enum import Enum

class NoteSelectionMode(Enum):
    ONE_CLICKED_NOTE = 1
    MANY_CLICKED_NOTES = 2
    BY_RECT_RANGE = 3
    BY_ADDING_NEIGHBOR = 4
    BY_MEASURES = 5