from datetime import timedelta
from enum import Enum
from typing import List

import humanize  # type: ignore
from rich.console import RenderableType, RenderGroup
from rich.markup import escape
from rich.progress import ProgressColumn, Task
from rich.progress_bar import ProgressBar
from rich.table import Table
from rich.text import Text

from layer.projects.entity import Entity, EntityStatus
from layer.projects.tracker.resource_transfer_state import ResourceTransferState


class ProgressStyle(str, Enum):
    NONE = ""

    GREY = "rgb(161,161,169)"
    GREEN = "rgb(52,211,153)"
    ORANGE = "rgb(251,147,60)"
    BLUE = "rgb(123,121,189)"

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
        EntityStatus.RESOURCE_UPLOADING: ProgressStyle.NONE,
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
            + 28
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

    @staticmethod
    def _render_state(state: ResourceTransferState) -> Text:
        num_files_uploaded = (
            f"{state.transferred_num_files}/{state.total_num_files} files"
        )
        at_least_a_gig = state.total_resource_size_bytes > 1_000_000_000
        size_format = "%.1f" if at_least_a_gig else "%.f"
        transferred_bytes = humanize.naturalsize(
            state.transferred_resource_size_bytes, format=size_format
        )
        total_resources_bytes = humanize.naturalsize(
            state.total_resource_size_bytes, format=size_format
        )
        bytes_uploaded = f"{transferred_bytes}/{total_resources_bytes}"
        if state.transferred_num_files < state.total_num_files:
            bandwidth = f"|{humanize.naturalsize(state.get_bandwidth_in_previous_seconds(), format='%.1f')}/s"
        else:
            bandwidth = ""
        return Text.from_markup(f"{num_files_uploaded}|{bytes_uploaded}{bandwidth}")

    def _render_progress_bar(self, task: Task) -> RenderableType:
        entity = self._get_entity(task)
        style_map = {
            EntityStatus.PENDING: (True, "default", ProgressStyle.DONE),
            EntityStatus.SAVING: (True, "default", ProgressStyle.DONE),
            EntityStatus.BUILDING: (False, "default", ProgressStyle.DONE),
            EntityStatus.TRAINING: (False, "default", ProgressStyle.DONE),
            EntityStatus.DONE: (False, ProgressStyle.DONE, ProgressStyle.DONE),
            EntityStatus.ERROR: (False, ProgressStyle.ERROR, ProgressStyle.ERROR),
            EntityStatus.ASSERTING: (True, "default", ProgressStyle.DONE),
            EntityStatus.RESOURCE_UPLOADING: (False, "default", ProgressStyle.BLUE),
        }
        pulse, style, completed_style = style_map.get(
            entity.status, (False, "default", ProgressStyle.DONE)
        )

        if entity.status == EntityStatus.RESOURCE_UPLOADING:
            assert entity.resource_transfer_state
            state = entity.resource_transfer_state
            completed = (
                state.transferred_resource_size_bytes / state.total_resource_size_bytes
            )
            task.completed = int(task.total * completed)

        return ProgressBar(
            total=max(0.0, task.total),
            completed=max(0.0, task.completed),
            width=22,
            animation_time=task.get_time(),
            style=style,
            pulse=pulse,
            complete_style=completed_style,
            finished_style=completed_style,
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
        if entity.status == EntityStatus.RESOURCE_UPLOADING:
            assert entity.resource_transfer_state
            color = "blue"
            delta = timedelta(seconds=entity.resource_transfer_state.get_eta_seconds())
        else:
            color = "yellow"
            delta = timedelta(seconds=self._get_elapsed_time_s(task))
        if entity.status == EntityStatus.PENDING:
            return Text.from_markup(f"[ [{color}]-:--:--[/{color}] ]", style="default")
        return Text.from_markup(f"[ [{color}]{delta}[/{color}] ]", style="default")

    def _render_description(self, task: Task) -> Text:
        entity = self._get_entity(task)
        if (
            entity.resource_transfer_state
            and entity.status == EntityStatus.RESOURCE_UPLOADING
        ):
            text = self._render_state(entity.resource_transfer_state)
            text.justify = "center"
            text.overflow = "fold"
            return text
        else:
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
