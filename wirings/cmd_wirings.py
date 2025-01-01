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
     ])

root_kbd_resolver = KbdResolver([score_view_bindings])