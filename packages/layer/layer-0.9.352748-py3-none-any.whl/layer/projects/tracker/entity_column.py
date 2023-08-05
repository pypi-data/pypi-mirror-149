from datetime import timedelta
from enum import Enum
from typing import List

from rich.console import RenderableType, RenderGroup
from rich.markup import escape
from rich.progress import ProgressColumn, Task
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text

from layer.projects.entity import Entity, EntityStatus


class ProgressStyle(str, Enum):
    NONE = ""

    GREY = "rgb(161,161,169)"
    GREEN = "rgb(52,211,153)"
    ORANGE = "rgb(251,147,60)"

    LINK = f"underline {GREY}"
    PENDING = GREY
    DONE = GREEN
    ERROR = ORANGE


class EntityColumn(ProgressColumn):
    _status_style_map = {
        EntityStatus.PENDING: ProgressStyle.NONE,
        EntityStatus.SAVING: ProgressStyle.NONE,
        EntityStatus.BUILDING: ProgressStyle.NONE,
        EntityStatus.TRAINING: ProgressStyle.NONE,
        EntityStatus.DONE: ProgressStyle.DONE,
        EntityStatus.ERROR: ProgressStyle.ERROR,
        EntityStatus.ASSERTING: ProgressStyle.NONE,
    }

    def render(self, task: Task) -> RenderableType:
        entity = self._get_entity(task)
        table = Table.grid(padding=(0, 1, 0, 1), pad_edge=True)
        table.add_column(width=20)  # name
        table.add_column()  # bar
        table.add_column(  # task description
            width=max(  # pytype: disable=missing-parameter
                len(s.value)
                for s in EntityStatus  # https://youtrack.jetbrains.com/issue/PY-36205
            )
            + 12
        )
        table.add_column()  # elapsed
        table.add_row(
            entity.name,
            self._render_progress_bar(task),
            self._render_description(task),
            self._render_time(task),
        )
        renderables: List[RenderableType] = [table]
        if entity.url:
            table = Table.grid(padding=(0, 1, 0, 1), pad_edge=True)
            table.add_column()
            table.add_row(self._render_url(entity))
            renderables.append(table)
        if entity.error_reason:
            table = Table.grid(padding=(0, 1, 0, 1), pad_edge=True)
            table.add_column(overflow="fold")
            table.add_row(Text.from_markup(f"[red]{escape(entity.error_reason)}[/red]"))
            table.add_row(Text("Aborting...", style="bold"))
            renderables.append(table)
        return RenderGroup(*renderables)

    def _render_progress_bar(self, task: Task) -> RenderableType:
        entity = self._get_entity(task)
        style_map = {
            EntityStatus.PENDING: (True, "default"),
            EntityStatus.SAVING: (True, "default"),
            EntityStatus.BUILDING: (False, "default"),
            EntityStatus.TRAINING: (False, "default"),
            EntityStatus.DONE: (False, ProgressStyle.DONE),
            EntityStatus.ERROR: (False, ProgressStyle.ERROR),
            EntityStatus.ASSERTING: (True, "default"),
        }
        pulse, style = style_map.get(entity.status, (False, "default"))

        return ProgressBar(
            total=max(0.0, task.total),
            completed=max(0.0, task.completed),
            width=22,
            animation_time=task.get_time(),
            style=style,
            pulse=pulse,
            complete_style=ProgressStyle.DONE,
            finished_style=ProgressStyle.DONE,
            pulse_style=ProgressStyle.PENDING,
        )

    @staticmethod
    def _get_entity(task: Task) -> Entity:
        return task.fields["entity"]

    @staticmethod
    def _get_elapsed_time_s(task: Task) -> int:
        elapsed_time = task.finished_time if task.finished else task.elapsed
        return int(elapsed_time) if elapsed_time else 0

    def _render_time(self, task: Task) -> RenderableType:
        entity = self._get_entity(task)
        if entity.status == EntityStatus.PENDING:
            return Text.from_markup("[ [yellow]-:--:--[/yellow] ]", style="default")
        delta = timedelta(seconds=self._get_elapsed_time_s(task))
        return Text.from_markup(f"[ [yellow]{delta}[/yellow] ]", style="default")

    def _render_description(self, task: Task) -> Text:
        entity = self._get_entity(task)
        return Text(
            task.description,
            overflow="fold",
            style=self._status_style_map[entity.status],
            justify="center",
        )

    @staticmethod
    def _render_url(entity: Entity) -> RenderableType:
        return RenderGroup(
            *[
                Text.from_markup(
                    f"[link={str(entity.url)}]{str(entity.url)}[/link]",
                    style=ProgressStyle.LINK,
                    overflow="fold",
                    justify="default",
                )
            ]
        )
