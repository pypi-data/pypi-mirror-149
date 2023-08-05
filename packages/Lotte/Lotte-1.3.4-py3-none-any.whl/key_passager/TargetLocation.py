class TargetLocation:
    def __init__(self, my_id, start, end, text):
        self.my_id = my_id
        self.start = start
        self.end = end
        self.text = text

    def __hash__(self) -> int:  # pragma: no cover
        return hash((self.my_id, self.start, self.end))

    def __eq__(self, other):  # pragma: no cover
        if not isinstance(other, TargetLocation):
            return NotImplemented

        return self.my_id == other.my_id
