
class Cell:
    def __init__(self, y, x):
        self.status = 0
        self.neighbors = []
        self.coords = (y, x)

    @property
    def live_neighbors(self):
        return sum(map(lambda x: x.status, self.neighbors))
