from dataclasses import dataclass
from quid.match.MatchSpan import MatchSpan


@dataclass
class Match:
    source_span: MatchSpan
    target_span: MatchSpan
