class Position(object):
    def __init__(self, key, desc = None):
        self.key = key
        self.description = desc
        self.x = None
        self.y = None
        self.x1 = None
        self.y1 = None

    def set_position(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def set_end_position(self, x, y):
        self.x1 = int(x)
        self.y1 = int(y)

    def to_dict(self):
        return {
            'key': self.key,
            'desc': self.description,
            'x': self.x,
            'y': self.y
        }