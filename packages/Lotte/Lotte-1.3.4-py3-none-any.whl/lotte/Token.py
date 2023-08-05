from dataclasses import dataclass


@dataclass
class Token:
    text: str
    start_pos: int
    end_pos: int
