from dataclasses import dataclass
from typing import List

from quid.passager.CitationSource import CitationSource
from quid.passager.CitationSourceLink import CitationSourceLink
from quid.passager.TargetText import TargetText
from quid.passager.TargetTextLocationLink import TargetTextLocationLink


@dataclass(frozen=True)
class AnalyzedWork:
    citation_sources: List[CitationSource]
    target_texts: List[TargetText]
    target_text_location_links: List[TargetTextLocationLink]
    citation_source_links: List[CitationSourceLink]
