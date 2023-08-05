class Field:
    def __init__(self, name: str):
        # PostgreSQL Notation
        self.name = f'"{name}"'

