from dataclasses import dataclass
from typing import List

from key_passager.ImportantSegment import ImportantSegment
from key_passager.SourceSegment import SourceSegment


@dataclass
class CitationSource:
    my_id: int
    source_segments: List[SourceSegment]
    important_segments: List[ImportantSegment] = None
    text: str = ''

    @classmethod
    def from_segment(cls, my_id, segment):
        return cls(my_id, [segment])

    def add_segment_to_start(self, segment):
        self.source_segments.insert(0, segment)

    def add_segment_to_end(self, segment):
        self.source_segments.insert(len(self.source_segments), segment)

    def get_start(self):
        return self.source_segments[0].start

    def get_end(self):
        return self.source_segments[-1].end
