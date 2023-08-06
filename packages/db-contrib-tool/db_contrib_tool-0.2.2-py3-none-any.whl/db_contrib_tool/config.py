"""Common config module."""
from __future__ import annotations

import os
from enum import Enum
from typing import Any, Dict, List, Optional, Set

from evergreen import Task
from pydantic import BaseModel

from db_contrib_tool.utils.filesystem import read_yaml_file

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
SETUP_REPRO_ENV_CONFIG_FILE = os.path.join(CONFIG_DIR, "setup_repro_env_config.yml")
# Records the paths of installed multiversion binaries on Windows.
WINDOWS_BIN_PATHS_FILE = "windows_binary_paths.txt"


class SegmentWriteKey(Enum):
    DEV = "RmMosrk1bf025xLRbZUxF2osVzGLPpL3"
    PROD = "jrHGRmtQBO8HYU1CyCfnB279SnktLgGH"


SEGMENT_WRITE_KEY = SegmentWriteKey.PROD.value
if os.environ.get("ENV") == "DEV":
    SEGMENT_WRITE_KEY = SegmentWriteKey.DEV.value


class Tasks(BaseModel):
    """
    Important evergreen tasks for setup repro env config.

    * binary: Set of tasks that create mongo binaries.
    * symbols: Set of tasks that publish debug symbols.
    * push: Set of tasks that push artifacts.
    """

    binary: Set[str]
    symbols: Set[str]
    push: Set[str]

    def is_task_binary(self, evg_task: Task) -> bool:
        """Determine if the given evergreen task generates mongo binaries."""
        return evg_task.display_name in self.binary

    def is_task_symbols(self, evg_task: Task) -> bool:
        """Determine if the given evergreen task generates debug symbols."""
        return evg_task.display_name in self.symbols

    def is_task_push(self, evg_task: Task) -> bool:
        """Determine if the given evergreen task pushes artifacts."""
        return evg_task.display_name in self.push


class Buildvariant(BaseModel):
    """Class represents evergreen buildvariant in setup repro env config."""

    name: str
    edition: str
    platform: str
    architecture: str
    versions: Optional[List[str]] = None


class SetupReproEnvConfig(BaseModel):
    """Class represents setup repro env config."""

    evergreen_tasks: Tasks
    evergreen_buildvariants: List[Buildvariant]

    @classmethod
    def from_yaml_file(cls, filename: str) -> SetupReproEnvConfig:
        """Create an instance of the class from the given filename."""
        return cls(**read_yaml_file(filename))


SETUP_REPRO_ENV_CONFIG = SetupReproEnvConfig.from_yaml_file(SETUP_REPRO_ENV_CONFIG_FILE)
