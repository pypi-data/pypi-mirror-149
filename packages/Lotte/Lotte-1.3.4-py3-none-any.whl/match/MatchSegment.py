from dataclasses import dataclass


@dataclass
class MatchSegment:
    character_start_pos: int
    character_end_pos: int
    text: str = ''
