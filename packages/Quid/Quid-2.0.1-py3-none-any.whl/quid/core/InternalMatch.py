from dataclasses import dataclass
from quid.core.InternalMatchSpan import InternalMatchSpan


@dataclass
class InternalMatch:
    source_match_span: InternalMatchSpan
    target_match_span: InternalMatchSpan
