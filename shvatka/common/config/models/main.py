from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from shvatka.common.config.models.paths import Paths
from shvatka.infrastructure.db.config.models.db import DBConfig, RedisConfig


@dataclass
class Config:
    paths: Paths
    db: DBConfig
    redis: RedisConfig
    file_storage_config: FileStorageConfig

    @property
    def app_dir(self) -> Path:
        return self.paths.app_dir

    @property
    def config_path(self) -> Path:
        return self.paths.config_path

    @property
    def log_path(self) -> Path:
        return self.paths.log_path


@dataclass
class FileStorageConfig:
    path: Path
    mkdir: bool
    parents: bool
    exist_ok: bool
