import random
from PyQt5.QtGui import QColor

class Note:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    @staticmethod
    def random_note(width, height):
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        return Note(x, y, color)