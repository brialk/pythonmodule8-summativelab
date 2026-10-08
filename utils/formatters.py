from tabulate import tabulate


def format_project_summary(project):
    """Return a readable string describing a project and its tasks."""
    lines = [
        f"Project: {project.title}",
        f"Owner: {project.user.name}",
        f"Description: {project.description or 'None'}",
        f"Due date: {project.due_date or 'None'}",
        ""
    ]

    if not project.tasks:
        lines.append("No tasks yet.")
    else:
        rows = [[task.id, task.title, task.status, task.assigned_to or "Unassigned"] for task in project.tasks]
        lines.append(tabulate(rows, headers=["ID", "Title", "Status", "Assigned To"]))

    return "\n".join(lines)


def format_project_list(projects):
    """Return a readable table of projects."""
    if not projects:
        return "No projects found."

    rows = [[p.id, p.title, p.user.name, len(p.tasks)] for p in projects]
    return tabulate(rows, headers=["ID", "Title", "Owner", "Tasks"])