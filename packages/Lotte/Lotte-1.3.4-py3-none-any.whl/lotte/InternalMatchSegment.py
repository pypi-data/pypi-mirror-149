class InternalMatchSegment:
    def __init__(self, token_start_pos: int, token_length: int, character_start_pos: int, character_end_pos: int):
        self.token_start_pos = token_start_pos
        self.token_length = token_length
        self.character_start_pos = character_start_pos
        self.character_end_pos = character_end_pos

    def __str__(self):  # pragma: no cover
        return "MatchSegment (" + str(self.character_start_pos) + ", " + str(self.character_end_pos) + ")"
