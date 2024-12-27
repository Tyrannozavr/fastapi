class MyExcellentException(Exception):
    def __init__(self, name: str|None = None):
        self.name = name

