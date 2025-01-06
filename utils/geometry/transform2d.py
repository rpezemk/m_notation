class T2D:
    def __init__(self, x = None, y = None):
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0


    def __add__(a: 'T2D', b: 'T2D'):
        return T2D(a.x + b.x, a.y + b.y)
    def __sub__(a: 'T2D', b: 'T2D'):
        return T2D(a.x - b.x, a.y - b.y)

    def __mul__(a: 'T2D', b: float):
        return T2D(a.x * b, a.y * b)

    def __str__(self):
        """User-friendly string for the object."""
        return f"x={self.x}, y={self.y}"

    def __repr__(self):
        """Developer-friendly string for the object."""
        return f"x={self.x}, y={self.y}"

    def add_x(self, x: int):
        res = T2D(self.x + x, self.y)
        return res

    def add_y(self, y: int):
        res = T2D(self.x, self.y+y)
        return res

# t1 = Transform2D(10, 2)

# t2 = Transform2D(20, 9)

# t3 = t1 * 100

# print(t3)
