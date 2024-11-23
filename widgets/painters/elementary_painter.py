class ElementaryPainter():    
    def paint(self, transform, q_painter):
        ...

class HeadPainter(ElementaryPainter):
    def paint(self, transform, q_painter):
        return super().paint(transform, q_painter)
    
    
class BeamPainter(ElementaryPainter):
    def paint(self, transform, q_painter):
        return super().paint(transform, q_painter)

class FlagPainter(ElementaryPainter):
    def paint(self, transform, q_painter):
        return super().paint(transform, q_painter)

