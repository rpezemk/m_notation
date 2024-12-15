from utils.file_utils.fs_model import DirModel, ParentDirModel, get_tree
from widgets.views.my_table_widget import MyTableView, finish_path
from wirings.test_methods import quit_csound, save_file, start_CSOUND, play_ding, static_play_file, play_file

import os
from typing import Any, Callable


class FileTable(MyTableView):
    def __init__(self, on_path_changed_func: Callable[[str], None] = None):
        self.on_path_changed_func = on_path_changed_func
        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        self.current_path = resolved_path
        self.dir_model = DirModel(abs_path=self.current_path)
        self.on_path_changed(self.dir_model.abs_path)
        columns = [
                ("d", 15, True, None, None),
                ("rel_path", 400, True, None, self.double_click_change_dir),
                ("ext", 60, True, None, None),
                ("play", 60, True, self.play_click, None)
            ]

        super().__init__(columns,
                         get_data_func=self.get_data,
                         on_selection_changed=self.on_selection_changed)

    def get_data(self):
        ok, self.dir_children = get_tree(self.dir_model)
        data = [["D" if isinstance(fsi, DirModel) or isinstance(fsi, ParentDirModel) else "F", finish_path(fsi), fsi.ext, (self.txt_for_play(fsi) )] for fsi in self.dir_children]
        return data

    def txt_for_play(self, fsi):
        return "PLAY" if fsi.ext in [".wav", ".wave"] else "< >"

    def play_click(self, row_data: list[Any], row_idx):
        if not row_data or len(row_data) == 0:
            return

        fs_item = self.dir_children[row_idx]
        if fs_item.ext in [".wav", ".wave"]:
            play_file(fs_item.abs_path)
        print(f"TEST CLICK PLAY row_idx:{row_idx}")

    def double_click_change_dir(self, row_data: list[Any], row_idx):
        if not row_data or len(row_data) == 0:
            return

        fs_item = self.dir_children[row_idx]
        if isinstance(fs_item, DirModel) or isinstance(fs_item, ParentDirModel):
            self.dir_model = fs_item
            self.on_path_changed(self.dir_model.abs_path)
        self.refresh_view()

    def on_selection_changed(self, selected, deselected):
            selected_rows = [index.row() for index in self.table_widget.selectedIndexes()]
            print(f"Selected rows: {selected_rows}")

    def on_path_changed(self, path: str):
        if self.on_path_changed_func:
            self.on_path_changed_func(str(path))