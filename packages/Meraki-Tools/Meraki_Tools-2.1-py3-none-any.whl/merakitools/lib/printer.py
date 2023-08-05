
class Printer:
    def __init__(self):
        self.contents = []

    def write(self, value):
        self.contents.append(value)