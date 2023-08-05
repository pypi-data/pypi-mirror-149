from dataclasses import dataclass
from lotte.InternalMatchSegment import InternalMatchSegment


@dataclass
class InternalMatch:
    source_match_segment: InternalMatchSegment
    target_match_segment: InternalMatchSegment
