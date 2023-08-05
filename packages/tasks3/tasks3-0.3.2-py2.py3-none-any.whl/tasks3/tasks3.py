"""Main module."""

from functools import singledispatch
from typing import List

from tasks3.db import Task, session_scope

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Query


@singledispatch
def add(
    title: str,
    urgency: int,
    importance: int,
    tags: List[str],
    folder: str,
    description: str,
    db_engine: Engine,
) -> str:
    """Add a task

    :param title: Title for the new task.
    :param urgency: Urgency level[0-4] for the new task.
    :param importance: Importance level[0-4] for the new task.
    :param tags: Set of tags to apply to the new task.
    :param folder: Delegate this task to a particular directory or file.
    :param description: Description of the task.
    :param db_engine: Engine for the tasks database.
    """
    task = Task(
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        folder=folder,
        description=description,
    )
    return add(task, db_engine)


@add.register(Task)
def _(
    task: Task,
    db_engine: Engine,
) -> str:
    """Add a task

    :param task: Task to add.
    :param db_engine: Engine for the tasks database.
    """
    with session_scope(db_engine) as session:
        session.add(task)
        session.flush()
        return task.id


def edit(
    id: str,
    db_engine: Engine,
    title: str = None,
    urgency: int = None,
    importance: int = None,
    tags: List[str] = None,
    folder: str = None,
    description: str = None,
):
    """Edit a task

    :param id: ID of the task to edit.
    :param db_engine: Engine for the tasks database.
    :param title: Update title of the task.
    :param urgency: Update urgency level[0-4] of the task.
    :param importance: Update importance level[0-4] of the task.
    :param tags: Set of tags to apply to the new task.
    :param folder: Delegate this task to a particular directory or file.
    :param description: Description of the task.
    """
    with session_scope(db_engine) as session:
        task: Task = Query(Task, session).filter_by(id=id).one()
        if title:
            task.title = title
        if urgency:
            task.urgency = urgency
        if importance:
            task.importance = importance
        if tags:
            task.tags = tags
        if folder:
            task.folder = folder
        if description:
            task.description = description
        session.add(task)


def remove(id: str, db_engine: Engine) -> Task:
    """Remove a Task

    :param id: ID of the task to remove.
    :param db_engine: Engine for the tasks database.
    """
    with session_scope(db_engine) as session:
        task: Task = Query(Task, session).filter_by(id=id).one()
        session.delete(task)
    return task
