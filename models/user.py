from models.person import Person


class User(Person):
    """Represents a user who owns one or more projects."""

    all = []
    _next_id = 1

    def __init__(self, name, email=None, user_id=None):
        super().__init__(name)
        self.email = email
        self.projects = []

        if user_id is None:
            self.id = User._next_id
            User._next_id += 1
        else:
            self.id = user_id
            User._next_id = max(User._next_id, user_id + 1)

        User.all.append(self)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if value is None or not str(value).strip():
            self._email = "Unknown"
        elif isinstance(value, str) and "@" in value:
            self._email = value
        else:
            raise ValueError("email must be a valid string containing '@'")

    def add_project(self, project):
        self.projects.append(project)

    @classmethod
    def find_by_name(cls, name):
        for user in cls.all:
            if user.name.lower() == name.lower():
                return user
        return None

    @classmethod
    def clear_all(cls):
        cls.all = []
        cls._next_id = 1

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}', projects={len(self.projects)})"