from dataclasses import dataclass
from match.MatchSegment import MatchSegment


@dataclass
class Match:
    source_match_segment: MatchSegment
    target_match_segment: MatchSegment
