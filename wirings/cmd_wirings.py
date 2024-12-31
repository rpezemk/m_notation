from utils.commands.command_containter import CommandContainer
from utils.commands.kbd_resolver import KbdResolver
from widgets.views.score_view import ScoreView
from wirings.cmd_definitions import *


score_view_bindings = CommandContainer.for_widget(ScoreView).define_bindings(
    [
        (C_NEXT, lambda v: v.select_next_note()),
        (C_PREV, lambda v: v.select_prev_note()),
        (C_UP, lambda v: v.select_note_above()),
        (C_DOWN, lambda v: v.select_note_below()),
     ])

root_kbd_resolver = KbdResolver([score_view_bindings])