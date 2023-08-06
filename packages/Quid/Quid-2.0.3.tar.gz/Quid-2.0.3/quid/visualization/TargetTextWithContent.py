from dataclasses import dataclass
from quid.passager import TargetText


@dataclass(frozen=True)
class TargetTextWithContent:
    target_text: TargetText
    content: str
