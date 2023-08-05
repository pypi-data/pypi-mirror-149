"""Console script for tasks3."""
import sys

import tasks3
import tasks3.db

import click
import sqlalchemy

from pathlib import Path
from typing import Optional, Iterable

from tasks3.config import config
from tasks3.db import Task

from pkg_resources import iter_entry_points
from click_plugins import with_plugins


@with_plugins(iter_entry_points("click_command_tree"))
@click.group()
@click.option(
    "--db",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=config.db_path,
    show_default=True,
    help="Location of tasks database.",
)
@click.version_option()
@click.pass_context
def main(ctx: click.core.Context, db: Path):
    """tasks3 is a commandline tool to create and manage tasks and todo lists"""

    ctx.ensure_object(dict)
    config.db_path = db
    engine = sqlalchemy.create_engine(config.db_uri)
    tasks3.db.init(db_engine=engine)
    ctx.obj["config"] = config
    ctx.obj["engine"] = engine
    return 0


@main.group()
@click.pass_context
def task(ctx: click.core.Context):
    """Manage a task"""
    pass


@task.command()
@click.option(
    "--id",
    type=str,
    help="Filter by id. "
    "You can pass /partial-id/ to search for all tasks whose id contains partial-id.",
)
@click.option("-T", "--title", type=str, help="Search by Title")
@click.option(
    "-u",
    "--urgency",
    type=click.IntRange(min=0, max=4, clamp=True),
    help="Filter by urgency.",
)
@click.option(
    "-i",
    "--importance",
    type=click.IntRange(min=0, max=4, clamp=True),
    help="Filter by importance.",
)
@click.option("-t", "--tags", multiple=True, help="Filter by tags.")
@click.option(
    "-f",
    "--folder",
    type=click.Path(readable=False, resolve_path=True, path_type=Path),
    help="Filter by delegated folder.",
)
@click.option("-d", "--description", type=str, help="Search in description.")
@click.pass_context
def search(
    ctx: click.core.Context,
    id: str,
    title: str,
    urgency: int,
    importance: int,
    tags: list,
    folder: str,
    description: str,
):
    """Search for tasks"""
    pass


@task.command()
@click.option(
    "-f",
    "--format",
    type=click.Choice(["YAML"]),
    default="YAML",
    help="Output format.",
    show_default=True,
)
@click.argument("id", type=str, required=False)
@click.pass_context
def show(ctx: click.core.Context, format: str, id: str):
    """Show the task in the specified FORMAT

    ID is the id of the Task to be printed.
    """
    pass


@task.command()
@click.option(
    "--yes",
    default=False,
    help="Overwrite task data without confirmation?",
)
@click.argument("id", type=str)
@click.pass_context
def edit(ctx: click.core.Context, yes: bool, id: str):
    """Edit a Task

    ID is the id of the Task to be edited.
    """
    pass


@task.command()
@click.option(
    "--yes",
    default=False,
    help="Delete task without confirmation?",
)
@click.argument("id", type=str)
@click.pass_context
def remove(ctx: click.core.Context, yes: bool, id: str):
    """Remove a Task

    ID is the id of the Task to be removed.
    """
    pass


@task.command()
@click.option(
    "-T", "--title", default="Give a Title to this Task.", help="Title of the Task."
)
@click.option(
    "-u",
    "--urgency",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    show_default=True,
    help="Level of urgency of the Task. " "Higher is more urgent.",
)
@click.option(
    "-i",
    "--importance",
    type=click.IntRange(min=0, max=4, clamp=True),
    default=2,
    show_default=True,
    help="Level of importance of the Task. " "Higher is more important.",
)
@click.option("-t", "--tags", multiple=True, default=[], help="Tags for the Task.")
@click.option(
    "-f",
    "--folder",
    type=click.Path(readable=False, resolve_path=True, path_type=Path),
    default=Path.cwd(),
    help=(
        "Delegate Task to a specified directory or file.  "
        "[default: current working directory]"
    ),
)
@click.option(
    "-d", "--description", default="", help="A short description of the Task."
)
@click.option(
    "--yes",
    default=False,
    is_flag=True,
    help="Create task without confirmation?",
)
@click.pass_context
def add(
    ctx: click.core.Context,
    title: str,
    urgency: int,
    importance: int,
    tags: Iterable[str],
    folder: Path,
    description: Optional[str],
    yes: bool,
):
    """Add a new task"""
    engine = ctx.obj["engine"]
    description = description.replace("\\n", "\n").replace("\\t", "\t")
    task = Task(
        title=title,
        urgency=urgency,
        importance=importance,
        tags=tags,
        folder=str(folder),
        description=description,
    )
    if not yes:
        click.confirm(
            f"{task.yaml()}\nAre you sure you want to add this task?",
            abort=True,
            default=True,
        )
    tasks3.add(task, db_engine=engine)
    click.echo(f"Added Task:\n{task.short()}")


@main.group()
@click.pass_context
def db(ctx: click.core.Context):
    """Manage tasks3's database"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to purge all tasks?")
@click.pass_context
def purge(ctx: click.core.Context):
    """Purge all tasks from the database"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to drop the database?")
@click.pass_context
def drop(ctx: click.core.Context):
    """Drop the databse"""
    pass


@db.command()
@click.confirmation_option(prompt="Are you sure you want to move the database?")
@click.argument(
    "dest_db",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=config.db_path,
)
@click.pass_context
def move(ctx: click.core.Context, dest_db: str):
    """Move tasks database to DEST_DB

    DEST_DB will be overwriten if it already exists.
    """
    pass


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
