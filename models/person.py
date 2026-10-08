class Person:
    """Base class for any individual tracked by the system."""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name