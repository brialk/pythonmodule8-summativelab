class Task:
    """Represents a single task that belongs to one project."""

    all = []
    _next_id = 1
    VALID_STATUSES = ("incomplete", "in-progress", "complete")

    def __init__(self, title, project, status="incomplete", assigned_to=None, task_id=None):
        self.title = title
        self.project = project
        self.status = status
        self.assigned_to = assigned_to

        if task_id is None:
            self.id = Task._next_id
            Task._next_id += 1
        else:
            self.id = task_id
            Task._next_id = max(Task._next_id, task_id + 1)

        Task.all.append(self)
        project.add_task(self)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value in self.VALID_STATUSES:
            self._status = value
        else:
            raise ValueError(f"status must be one of {self.VALID_STATUSES}")

    def complete(self):
        self.status = "complete"

    @classmethod
    def find_by_title_in_project(cls, project, title):
        for task in project.tasks:
            if task.title.lower() == title.lower():
                return task
        return None

    @classmethod
    def clear_all(cls):
        cls.all = []
        cls._next_id = 1

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}', assigned_to='{self.assigned_to}')"