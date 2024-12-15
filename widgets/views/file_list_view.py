import os
from typing import Any
from utils.file_utils.fs_model import DirModel, get_tree
from widgets.views.my_table_widget import MyTableView, finish_path




class FileListView(MyTableView):
    def __init__(self):

        current_dir = "."
        resolved_path = os.path.abspath(current_dir)
        self.current_path = resolved_path

        columns = [
                ("rel_path", 200, True, None, self.change_dir),
                ("ext", 20, True, None, None),
                ("play", 20, True, self.play_click, None)
            ]

        super().__init__(columns,
                         get_data_func=self.get_data,
                         on_selection_changed=self.on_selection_changed)

    def get_data(self):
        self.dir_model = DirModel(abs_path=self.current_path)
        ok, self.dir_children = get_tree(self.dir_model)
        data = [[finish_path(fs), fs.ext, fs.sel] for fs in self.dir_children]
        return data

    def play_click(self, row_data: list[Any]):
        print("TEST CLICK PLAY")

    def change_dir(self, row_data: list[Any]):
        print("TEST DOUBLE CLICK PLAY")

    def on_selection_changed(self, selected, deselected):
            selected_rows = [index.row() for index in self.table_widget.selectedIndexes()]
            print(f"Selected rows: {selected_rows}")