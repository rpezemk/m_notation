from utils.commands.command_containter import CommandContainer
from utils.commands.kbd_resolver import KbdResolver
from widgets.views.score_view import ScoreView
from widgets.views.score_view_modes import ScoreViewModeEnum
from wirings.cmd_definitions import *


score_view_bindings = CommandContainer         \
    .for_widget(ScoreView)                     \
    .for_mode(ScoreViewModeEnum.UNDEFINED)     \
    .define_bindings(    
    [
        (CMD_NEXT, lambda view: view.select_next_note()),
        (CMD_PREV, lambda view: view.select_prev_note()),
        (CMD_UP, lambda view: view.select_note_above()),
        (CMD_DOWN, lambda view: view.select_note_below()),
        (CMD_DEL, lambda view: view.delete_selected_notes()),
        
        (CMD_CTRL_NEXT, lambda view: view.select_next_note_in_next_measure()),
        (CMD_CTRL_PREV, lambda view: view.select_prev_note_in_prev_measure()),
        (CMD_ROTATE, lambda view: view.rotate_selected_notes()),
        (CMD_ESC, lambda view: view.deselect_notes_but([])),
        (C_SEL_VERTICAL_MEASURE, lambda view: view.select_vertical()),
        (C_SEL_HORIZONTAL_MEASURES, lambda view: view.select_horizontal()),
        (C_ADD_PREV_TO_SEL, lambda view: view.add_prev_to_sel()),
        (C_ADD_NEXT_TO_SEL, lambda view: view.add_next_to_sel()),
     ])

root_kbd_resolver = KbdResolver([score_view_bindings])

