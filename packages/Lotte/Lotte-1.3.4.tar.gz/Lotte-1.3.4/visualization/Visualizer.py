from typing import List

from yattag import Doc
from math import ceil

from key_passager.CitationSource import CitationSource
from visualization.Info import Info
import re

from visualization.TargetHtml import TargetHtml
from visualization.TargetTextWithContent import TargetTextWithContent
from visualization.Visualization import Visualization


# noinspection PyMethodMayBeStatic
class Visualizer:

    def __init__(self, censor: bool = False, keep_range: int = 25):
        self.censor = censor
        self.keep_range = keep_range

    def visualize(self, title, author, year, source_content: str, citation_sources: List[CitationSource],
                  citation_source_links, target_texts_with_content: List[TargetTextWithContent]) -> Visualization:

        info = self.__generate_info_json(title, author, year)
        source_html = self.__generate_source_html(source_content, citation_sources, citation_source_links)
        targets_html = self.__generate_target_html(target_texts_with_content)

        return Visualization(info, source_html, targets_html)

    def __generate_info_json(self, title, author, year) -> Info:
        return Info(title, author, year)

    def __calculate_max_target_texts_count(self, citation_source_links) -> int:
        max_citation_sources = 0

        for citation_source_link in citation_source_links:
            max_citation_sources = max(max_citation_sources, len(citation_source_link.target_location_selections))

        return max_citation_sources

    def __calculate_max_segment_frequency(self, citation_sources: List[CitationSource]) -> int:
        max_segment_frequency = 0

        for citation_source in citation_sources:
            for source_segment in citation_source.source_segments:
                max_segment_frequency = max(max_segment_frequency, source_segment.frequency)

        return max_segment_frequency

    def __generate_source_html(self, source_content: str, citation_sources: List[CitationSource],
                               citation_source_links) -> str:

        max_target_texts_count = self.__calculate_max_target_texts_count(citation_source_links)
        max_segment_frequency = self.__calculate_max_segment_frequency(citation_sources)

        doc, tag, text = Doc().tagtext()

        content = ''
        citation_source_start_pos = 0
        segments = []

        for char_pos in range(0, len(source_content)):
            finished = False
            for citation_source_pos in range(citation_source_start_pos, len(citation_sources)):
                citation_source = citation_sources[citation_source_pos]

                for segment_pos in range(0, len(citation_source.source_segments)):
                    segment = citation_source.source_segments[segment_pos]

                    if char_pos < segment.start:
                        finished = True
                        break

                    if segment.start == char_pos:
                        citation_source_start_pos = citation_source_pos

                        if segment_pos == 0:
                            with tag('span', klass='text_standard'):
                                doc.asis(content)
                            segments.clear()
                        else:
                            segments.append(('asis', content))

                        content = ''
                        finished = True
                        break
                    elif segment.end == char_pos or (segment_pos == len(citation_source.source_segments) - 1 and
                                                     char_pos == len(source_content) - 1):
                        citation_count = self.__calculate_target_text_count(citation_source, citation_source_links)
                        segment_frequency = segment.frequency
                        citation_count_percentage = \
                            int((ceil((citation_count / max_target_texts_count) * 10.0) / 10.0) * 10)
                        segment_frequency_percentage = \
                            int((ceil((segment_frequency / max_segment_frequency) * 10.0) / 10.0) * 10)
                        klass_background = f'source_segment_background_o{citation_count_percentage}'
                        klass_font = f'source_segment_font_s{segment_frequency_percentage}'
                        klass = f'source_segment {klass_background} {klass_font}'
                        tag_id = f'sourceSegment_{citation_source.my_id}_{segment.my_id}'
                        segments.append(('span', content, klass, tag_id, segment.token_length))
                        content = ''
                        finished = True

                        if segment_pos == len(citation_source.source_segments) - 1:
                            citation_source_start_pos += 1
                            with tag('span', klass='citation_source_container', id=str(citation_source.my_id)):
                                for segment in segments:
                                    if segment[0] == 'asis':
                                        if segment[1]:
                                            with tag('span', klass='text_standard'):
                                                doc.asis(segment[1])
                                    else:
                                        with tag('span', ('data-token-count', segment[4]), klass=segment[2],
                                                 id=segment[3]):
                                            doc.asis(segment[1])
                        break

                if finished:
                    break

            if source_content[char_pos] == '\n':
                content += '<br>'
            else:
                content += source_content[char_pos]

        if len(content) > 0:
            with tag('span', klass='text_standard'):
                doc.asis(content)

        return doc.getvalue()

    def __calculate_target_text_count(self, citation_source, citation_source_links):
        for citation_source_link in citation_source_links:
            if citation_source_link.citation_source_id == citation_source.my_id:
                return len(citation_source_link.target_location_selections)

        return None

    def __generate_target_html(self, target_texts_with_content: List[TargetTextWithContent]) -> List[TargetHtml]:

        result: List[TargetHtml] = []

        for target_text_with_content in target_texts_with_content:
            target_text = target_text_with_content.target_text
            target_content = target_text_with_content.content
            doc, tag, text = Doc().tagtext()

            content = ''
            location_start_pos = 0
            for char_pos in range(0, len(target_content)):
                for location_pos in range(location_start_pos, len(target_text.target_locations)):
                    location = target_text.target_locations[location_pos]

                    if char_pos < location.start:
                        break

                    if location.start == char_pos:
                        location_start_pos = location_pos
                        if self.censor:
                            if len(content) < self.keep_range * 2:
                                doc.asis(content)
                            else:
                                start = 0

                                if location_pos > 0:
                                    start = self.keep_range

                                content_replaced = re.sub("[A-Za-z0-9ÄÖÜäüöß]", "x", content[start:-self.keep_range])
                                doc.asis(content[0:start])
                                with tag('span', klass='censored'):
                                    doc.asis(content_replaced)
                                doc.asis(content[-self.keep_range:])
                        else:
                            doc.asis(content)
                        content = ''
                        break
                    elif location.end == char_pos:
                        with tag('span', klass='target_location', id=str(location.my_id)):
                            doc.asis(content)
                        content = ''
                        break

                if target_content[char_pos] == '\n':
                    content += '<br>'
                else:
                    content += target_content[char_pos]

            if len(content) > 0:
                if self.censor:
                    if len(content) < self.keep_range:
                        doc.asis(content)
                    else:
                        doc.asis(content[0:self.keep_range])
                        content = re.sub("[A-Za-z0-9ÄÖÜäüöß]", "x", content[self.keep_range:])
                        with tag('span', klass='censored'):
                            doc.asis(content)
                else:
                    doc.asis(content)

            result.append(TargetHtml(target_text.filename, doc.getvalue()))

        return result
