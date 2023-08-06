from typing import List
from dataclasses import dataclass

from argparse import Namespace

@dataclass
class RunningConfig:
    timeout: float
    destination_uri: str
    max_concurrency: int
    labels: List[str]
    debug: bool = False
    echo: bool = False
    no_display: bool = False
    banner: bool = False
    execution_rule: str = None

    @classmethod
    def from_cli(cls, parsed: Namespace):
        return cls(**{k: v for k, v in parsed.__dict__.items() if v is not None})

__all__ = ("RunningConfig", )
