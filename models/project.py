class Project:
    """Represents a project owned by a single user, containing many tasks."""

    all = []
    _next_id = 1

    def __init__(self, title, user, description="", due_date=None, project_id=None):
        self.title = title
        self.user = user
        self.description = description
        self.due_date = due_date
        self.tasks = []

        if project_id is None:
            self.id = Project._next_id
            Project._next_id += 1
        else:
            self.id = project_id
            Project._next_id = max(Project._next_id, project_id + 1)

        Project.all.append(self)
        user.add_project(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and value.strip():
            self._title = value.strip()
        else:
            raise ValueError("title must be a non-empty string")

    def add_task(self, task):
        self.tasks.append(task)

    @classmethod
    def find_by_title(cls, title):
        for project in cls.all:
            if project.title.lower() == title.lower():
                return project
        return None

    @classmethod
    def clear_all(cls):
        cls.all = []
        cls._next_id = 1

    def __repr__(self):
        return f"Project(id={self.id}, title='{self.title}', owner='{self.user.name}', tasks={len(self.tasks)})"