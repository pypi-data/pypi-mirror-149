from dataclasses import dataclass


@dataclass
class BestMatch:
    source_token_start: int
    target_token_start: int
    source_length: int
    target_length: int
