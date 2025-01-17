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
        (cmd([[Qt.Key_Right]]), lambda view: view.select_next_note()),
        (cmd([[Qt.Key_Left]]), lambda view: view.select_prev_note()),
        (cmd([[Qt.Key_Up]]), lambda view: view.select_note_above()),
        (cmd([[Qt.Key_Down]]), lambda view: view.select_note_below()),
        (cmd([[Qt.Key_Delete]]), lambda view: view.delete_selected_notes()),

        (cmd([[Qt.Key_Control, Qt.Key_Right]]), lambda view: view.select_next_note_in_next_measure()),
        (cmd([[Qt.Key_Control, Qt.Key_Left]]), lambda view: view.select_prev_note_in_prev_measure()),
        (cmd([[Qt.Key_Control, Qt.Key_R]]), lambda view: view.rotate_selected_notes()),
        (cmd([[Qt.Key_Escape]]), lambda view: view.deselect_notes_but([])),
        (cmd([[Qt.Key_Control, Qt.Key_T], [Qt.Key_Control, Qt.Key_V]]), lambda view: view.select_vertical()),
        (cmd([[Qt.Key_Control, Qt.Key_T], [Qt.Key_Control, Qt.Key_H]]), lambda view: view.select_horizontal()),
        (cmd([[Qt.Key_Control, Qt.Key_T], [Qt.Key_Control, Qt.Key_M]]), lambda view: view.select_single_measure()),
        (cmd([[Qt.Key_Shift, Qt.Key_Left]]), lambda view: view.add_prev_to_sel()),
        (cmd([[Qt.Key_Shift, Qt.Key_Right]]), lambda view: view.add_next_to_sel()),
        
        (cmd([[Qt.Key_Control, Qt.Key_T], [Qt.Key_Control, Qt.Key_T]]), lambda view: view.flip_tie()),

        (cmd([[Qt.Key_Control, Qt.Key_D]]), lambda view: view.oct_down()),
        (cmd([[Qt.Key_Control, Qt.Key_U]]), lambda view: view.oct_up()),
        
        (cmd([[Qt.Key_Control, Qt.Key_K]]), lambda view: view.name_down()),
        (cmd([[Qt.Key_Control, Qt.Key_I]]), lambda view: view.name_up()),
        (cmd([[Qt.Key_Shift, Qt.Key_K]]), lambda view: view.alter_down()),
        (cmd([[Qt.Key_Shift, Qt.Key_I]]), lambda view: view.alter_up()),
     ])



root_kbd_resolver = KbdResolver([score_view_bindings])

