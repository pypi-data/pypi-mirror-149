class File:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self._private = "hi"

    def print(self):
        print(self.x, self.y)