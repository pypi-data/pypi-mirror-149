from dataclasses import dataclass


@dataclass
class BestMatch:
    source_token_start_pos: int
    target_token_start_pos: int
    source_length: int
    target_length: int
