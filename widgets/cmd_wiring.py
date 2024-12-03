from utils.commands.command import SingleCmd


my_wirings = [
    SingleCmd("QUIT_APP", [Qt.Key_Control, Qt.Key_A], lambda: exit())
]