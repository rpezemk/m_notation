import sys
import os
import random
from typing import Tuple
# import PyQt5.QtGui
from PyQt5.QtGui import QFont, QFontDatabase

rel_font_path = "fonts/bravura/Bravura.otf"

class FontLoadError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


def try_get_music_font() -> Tuple[bool,QFont]:
    ok, res_font = False, None
    font_id = -1
    try:
        font_db = QFontDatabase()
        font_path = os.path.join(os.getcwd(), rel_font_path)
        font_id = font_db.addApplicationFont(font_path)
        if font_id == -1:
            raise FontLoadError(f"could not load {font_path} font file")
        font_family = font_db.applicationFontFamilies(font_id)[0]
        res_font = QFont(font_family, 35)
        res_font.setStyleStrategy(QFont.NoAntialias)
        ok = True
    except Exception as e:
        print(f"Error loading font: {e}")
        
    return ok, res_font
    