from dataclasses import dataclass
from typing import List

from key_passager.CitationSource import CitationSource
from key_passager.CitationSourceLink import CitationSourceLink
from key_passager.ImportantSegmentLink import ImportantSegmentLink
from key_passager.TargetText import TargetText
from key_passager.TargetTextLocationLink import TargetTextLocationLink


@dataclass(frozen=True)
class AnalyzedWork:
    citation_sources: List[CitationSource]
    target_texts: List[TargetText]
    target_text_location_links: List[TargetTextLocationLink]
    citation_source_links: List[CitationSourceLink]
    important_segment_links: List[ImportantSegmentLink]
