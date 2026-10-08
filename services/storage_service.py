import json
import os

from models.user import User
from models.project import Project
from models.task import Task

DATA_FILE = os.path.join("data", "project_data.json")


def save_data(filepath=DATA_FILE):
    """Serialize all users, projects, and tasks to a JSON file."""
    data = {"users": []}

    for user in User.all:
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "projects": []
        }

        for project in user.projects:
            project_data = {
                "id": project.id,
                "title": project.title,
                "description": project.description,
                "due_date": project.due_date,
                "tasks": []
            }

            for task in project.tasks:
                project_data["tasks"].append({
                    "id": task.id,
                    "title": task.title,
                    "status": task.status,
                    "assigned_to": task.assigned_to
                })

            user_data["projects"].append(project_data)

        data["users"].append(user_data)

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as file:
        json.dump(data, file, indent=2)


def load_data(filepath=DATA_FILE):
    """Load users, projects, and tasks from a JSON file, rebuilding relationships."""
    User.clear_all()
    Project.clear_all()
    Task.clear_all()

    if not os.path.exists(filepath):
        return

    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: could not read saved data. Starting with an empty workspace.")
        return

    for user_data in data.get("users", []):
        user = User(
            name=user_data["name"],
            email=user_data.get("email"),
            user_id=user_data["id"]
        )

        for project_data in user_data.get("projects", []):
            project = Project(
                title=project_data["title"],
                user=user,
                description=project_data.get("description", ""),
                due_date=project_data.get("due_date"),
                project_id=project_data["id"]
            )

            for task_data in project_data.get("tasks", []):
                Task(
                    title=task_data["title"],
                    project=project,
                    status=task_data.get("status", "incomplete"),
                    assigned_to=task_data.get("assigned_to"),
                    task_id=task_data["id"]
                )