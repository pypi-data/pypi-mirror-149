class InternalMatchSpan:
    def __init__(self, token_start: int, token_length: int, character_start: int, character_end: int):
        self.token_start_pos = token_start
        self.token_length = token_length
        self.character_start = character_start
        self.character_end = character_end

    def __str__(self):  # pragma: no cover
        return "MatchSpan (" + str(self.character_start) + ", " + str(self.character_end) + ")"
