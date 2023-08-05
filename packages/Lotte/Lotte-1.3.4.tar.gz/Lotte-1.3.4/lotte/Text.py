from dataclasses import dataclass


@dataclass
class Text:
    nr_of_characters: int
    nr_of_words: int
    tk_start_pos: int
    tk_end_pos: int
