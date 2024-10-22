class Position(object):
    def __init__(self, key):
        self.key = key
        self.x = None
        self.y = None
        self.x1 = None
        self.y1 = None

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_end_position(self, x, y):
        self.x1 = x
        self.y1 = y

    def to_dict(self):
        return {
            'key': self.key,
            'x': self.x,
            'y': self.y
        }