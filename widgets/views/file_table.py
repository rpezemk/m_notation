from utils.file_utils.fs_model import DirModel, ParentDirModel, get_tree
from widgets.views.my_table_widget import MyTableView, finish_path


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
                ("rel_path", 200, True, None, self.double_click_change_dir),
                ("ext", 20, True, None, None),
                ("play", 20, True, self.play_click, None)
            ]

        super().__init__(columns,
                         get_data_func=self.get_data,
                         on_selection_changed=self.on_selection_changed)

    def get_data(self):
        ok, self.dir_children = get_tree(self.dir_model)
        data = [["D" if isinstance(fsi, DirModel) or isinstance(fsi, ParentDirModel) else "F", finish_path(fsi), fsi.ext, "PLAY"] for fsi in self.dir_children]
        return data

    def play_click(self, row_data: list[Any], row_idx):
        if not row_data:
            return
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