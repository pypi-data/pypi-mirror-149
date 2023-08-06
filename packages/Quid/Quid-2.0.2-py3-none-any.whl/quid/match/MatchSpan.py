from dataclasses import dataclass


@dataclass
class MatchSpan:
    start: int
    end: int
    text: str = ''
