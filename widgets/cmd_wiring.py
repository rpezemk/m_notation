from utils.commands.command import MCmd


my_wirings = [
    MCmd("QUIT_APP", [Qt.Key_Control, Qt.Key_A], lambda: exit())
]