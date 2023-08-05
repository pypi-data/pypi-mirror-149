from dataclasses import dataclass
from typing import List
from quid.visualization.Info import Info
from quid.visualization.TargetHtml import TargetHtml


@dataclass(frozen=True)
class Visualization:
    info: Info
    source_html: str
    targets_html: List[TargetHtml]
