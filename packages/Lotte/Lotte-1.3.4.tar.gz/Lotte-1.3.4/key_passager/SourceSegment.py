class SourceSegment:
    def __init__(self, my_id, start, end, frequency, token_length, text):
        self.my_id = my_id
        self.start = start
        self.end = end
        self.frequency = frequency
        self.token_length = token_length
        self.text = text

    @classmethod
    def from_frequency(cls, my_id, start, end, frequency):
        return cls(my_id, start, end, frequency, 0, '')

    def increment_frequency(self):
        self.frequency += 1

    def __eq__(self, other):  # pragma: no cover
        if not isinstance(other, SourceSegment):
            return NotImplemented

        return self.my_id == other.my_id
