import numpy as np

class Transform2D:
    def __init__(self):
        self.matrix = np.eye(3)

    def translate(self, dx, dy):
        translation_matrix = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
        ])
        self.matrix = self.matrix @ translation_matrix

    def scale(self, sx, sy):
        scaling_matrix = np.array([
            [sx, 0, 0],
            [0, sy, 0],
            [0,  0, 1]
        ])
        self.matrix = self.matrix @ scaling_matrix

    def rotate(self, angle_rad):
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        rotation_matrix = np.array([
            [cos_a, -sin_a, 0],
            [sin_a,  cos_a, 0],
            [0,      0,     1]
        ])
        self.matrix = self.matrix @ rotation_matrix

    def apply(self, points):
        points_h = np.hstack([points, np.ones((len(points), 1))])
        transformed_points = points_h @ self.matrix.T
        return transformed_points[:, :2]

    def reset(self):
        self.matrix = np.eye(3)

    def get_matrix(self):
        return self.matrix