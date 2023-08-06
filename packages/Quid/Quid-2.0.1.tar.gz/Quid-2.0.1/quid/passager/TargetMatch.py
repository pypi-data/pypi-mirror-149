from dataclasses import dataclass


@dataclass
class TargetMatch:
    filename: str
    start: int
    end: int
