import argparse

from models.user import User
from models.project import Project
from models.task import Task
from services import storage_service
from services.ai_client import ProjectSummaryClient
from utils.formatters import format_project_list


def add_user(args):
    if User.find_by_name(args.name):
        print(f"User '{args.name}' already exists.")
        return
    user = User(name=args.name, email=args.email)
    storage_service.save_data()
    print(f"Added user: {user.name}")


def add_project(args):
    user = User.find_by_name(args.user)
    if user is None:
        print(f"User '{args.user}' not found. Add the user first with add-user.")
        return

    project = Project(title=args.title, user=user, description=args.description or "", due_date=args.due_date)
    storage_service.save_data()
    print(f"Added project '{project.title}' for {user.name}")


def add_task(args):
    project = Project.find_by_title(args.project)
    if project is None:
        print(f"Project '{args.project}' not found. Add the project first with add-project.")
        return

    task = Task(title=args.title, project=project, assigned_to=args.assigned_to)
    storage_service.save_data()
    print(f"Added task '{task.title}' to project '{project.title}'")


def list_projects(args):
    print(format_project_list(Project.all))


def complete_task(args):
    project = Project.find_by_title(args.project)
    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    task = Task.find_by_title_in_project(project, args.title)
    if task is None:
        print(f"Task '{args.title}' not found in project '{project.title}'.")
        return

    task.complete()
    storage_service.save_data()
    print(f"Marked task '{task.title}' as complete.")


def summarize_project(args):
    project = Project.find_by_title(args.project)
    if project is None:
        print(f"Project '{args.project}' not found.")
        return

    task_lines = "\n".join(
        f"- {task.title} ({task.status}), assigned to {task.assigned_to or 'Unassigned'}"
        for task in project.tasks
    ) or "No tasks yet."

    prompt = (
        "Summarize the status of this project in a few sentences, "
        "and suggest one next step.\n\n"
        f"Project: {project.title}\n"
        f"Description: {project.description or 'None'}\n"
        f"Due date: {project.due_date or 'None'}\n"
        f"Tasks:\n{task_lines}"
    )

    client = ProjectSummaryClient()
    summary = client.summarize(prompt)

    print(f"\n=== Summary for '{project.title}' ===")
    print(summary)


def build_parser():
    parser = argparse.ArgumentParser(description="Project Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("--name", required=True)
    add_user_parser.add_argument("--email", required=False)
    add_user_parser.set_defaults(func=add_user)

    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("--user", required=True)
    add_project_parser.add_argument("--title", required=True)
    add_project_parser.add_argument("--description", required=False)
    add_project_parser.add_argument("--due-date", dest="due_date", required=False)
    add_project_parser.set_defaults(func=add_project)

    add_task_parser = subparsers.add_parser("add-task", help="Add a new task")
    add_task_parser.add_argument("--project", required=True)
    add_task_parser.add_argument("--title", required=True)
    add_task_parser.add_argument("--assigned-to", dest="assigned_to", required=False)
    add_task_parser.set_defaults(func=add_task)

    list_projects_parser = subparsers.add_parser("list-projects", help="List all projects")
    list_projects_parser.set_defaults(func=list_projects)

    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task complete")
    complete_task_parser.add_argument("--project", required=True)
    complete_task_parser.add_argument("--title", required=True)
    complete_task_parser.set_defaults(func=complete_task)

    summarize_parser = subparsers.add_parser("summarize-project", help="Generate an AI summary of a project")
    summarize_parser.add_argument("--project", required=True)
    summarize_parser.set_defaults(func=summarize_project)

    return parser


def main():
    storage_service.load_data()

    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()