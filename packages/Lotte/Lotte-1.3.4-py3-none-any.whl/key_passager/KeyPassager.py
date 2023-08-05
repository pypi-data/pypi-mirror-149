import copy
import re
from typing import List, Dict

from key_passager.ImportantSegment import ImportantSegment
from key_passager.ImportantSegmentLink import ImportantSegmentLink
from key_passager.AnalyzedWork import AnalyzedWork
from key_passager.Location import Location
from key_passager.TargetMatch import TargetMatch
from key_passager.TextWithMatches import TextWithMatches
from key_passager.CitationSource import CitationSource
from key_passager.CitationSourceLink import CitationSourceLink
from key_passager.SourceSegment import SourceSegment
from key_passager.TargetLocation import TargetLocation
from key_passager.TargetLocationSelection import TargetLocationSelection
from key_passager.TargetText import TargetText
from key_passager.TargetTextLocationLink import TargetTextLocationLink


# noinspection PyMethodMayBeStatic
class KeyPassager:

    def __init__(self):
        self.next_id = 1

    def __generate_next_id(self) -> int:
        id_to_return = self.next_id
        self.next_id += 1
        return id_to_return

    def generate(self, texts_with_matches: List[TextWithMatches], source_text: str) -> AnalyzedWork:
        """
        Generate key passages from from matches between a source text and a number of target texts.
        :param texts_with_matches: A list of texts with the matches found by Lotte
        :param source_text: The source text
        :return: The results wrapped in an AnalyzedWork
        """
        citation_sources, segment_id_to_target_matches_map = self.__get_citation_sources(texts_with_matches,
                                                                                         source_text)
        self.__add_important_segments(citation_sources)

        target_texts, target_location_id_to_source_location_map = self.__generate_target_texts(texts_with_matches)
        target_text_location_links = \
            self.__generate_target_text_location_links(citation_sources, target_texts,
                                                       target_location_id_to_source_location_map)
        citation_source_links = self.__generate_citation_source_links(citation_sources, target_texts,
                                                                      segment_id_to_target_matches_map)

        important_segment_links = self.__generate_important_segment_links(citation_sources, target_texts,
                                                                          segment_id_to_target_matches_map)

        return AnalyzedWork(citation_sources, target_texts, target_text_location_links, citation_source_links,
                            important_segment_links)

    def __get_citation_sources(self, texts_with_matches: List[TextWithMatches], source_text) -> \
            (List[CitationSource], Dict[int, List[TargetMatch]]):
        """
        Get a list of CitationSources for all similarity files in the given similarity folder.
        :param texts_with_matches: A list of TextWithMatches
        :param source_text: The source text
        :return: A tuple where the first element is a list of CitationSources and the second element is a mapping from
        source segment ids to a list of TargetMatch.
        """

        citation_sources: List[CitationSource] = []
        segment_id_to_target_matches_map: Dict[int, List[TargetMatch]] = {}

        for target_text_matches in texts_with_matches:
            citation_sources, segment_id_to_target_matches_map = self.__get_citation_sources_from_file(
                target_text_matches,
                citation_sources,
                segment_id_to_target_matches_map)
        for citation_source in citation_sources:
            text = ''

            for segment in citation_source.source_segments:
                content = source_text[segment.start:segment.end].strip()
                length = len(content.split(' '))
                segment.token_length = length
                segment.text = content
                text += ' ' + content

            citation_source.text = text.strip()

        citation_sources.sort(key=lambda x: x.get_start())
        return citation_sources, segment_id_to_target_matches_map

    def __get_citation_sources_from_file(self, text_with_matches: TextWithMatches,
                                         citation_sources: List[CitationSource],
                                         segment_id_to_target_location_map) \
            -> (List[CitationSource], Dict[int, List[TargetMatch]]):
        """
        Get a list of citation sources for the given similarity file.
        :param text_with_matches: A list of TextWithMatches
        :param citation_sources: A list of already created CitationSources
        :param segment_id_to_target_location_map: A mapping from source segment ids to a list of TargetMatch
        :return: A tuple where the first element is a list of CitationSources and the second element is a mapping from
        source segment ids to a list of TargetMatch.
        """

        filename = text_with_matches.name
        for match in text_with_matches.matches:
            source_match_segment = match.source_match_segment
            target_match_segment = match.target_match_segment

            source_match_start = source_match_segment.character_start_pos
            source_match_end = source_match_segment.character_end_pos
            target_match_start = target_match_segment.character_start_pos
            target_match_end = target_match_segment.character_end_pos

            conflicting_sources = []
            conflicting_positions = []

            # Find conflicting sources, i.e. our new source would overlap with one or more existing sources.
            for i in range(0, len(citation_sources)):
                citation_source = citation_sources[i]
                if (citation_source.get_start() <= source_match_start < citation_source.get_end() or
                        citation_source.get_start() < source_match_end <= citation_source.get_end() or
                        source_match_start <= citation_source.get_start()
                        and source_match_end >= citation_source.get_end()):
                    conflicting_sources.append(citation_source)
                    conflicting_positions.append(i)

            # In case there are no conflicting sources, we can just create a new CitationSource.
            if len(conflicting_sources) == 0:
                new_id = self.__generate_next_id()
                new_segment = SourceSegment.from_frequency(new_id, source_match_start, source_match_end, 1)
                self.__add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                       target_match_end)

                new_citation_source = CitationSource.from_segment(self.__generate_next_id(), new_segment)

                new_citation_source_pos = len(citation_sources)
                if len(citation_sources) > 0:
                    for i in range(0, len(citation_sources)):
                        if source_match_end <= citation_sources[i].get_start():
                            new_citation_source_pos = i
                            break

                citation_sources.insert(new_citation_source_pos, new_citation_source)
            else:
                # It should be noted that new segments are created with a count of 0 and that the count is updated
                # in a later step.

                # In case there are conflicting sources, we need to check if the new match starts before the first
                # conflicting source. If that is the case, then we need to extend the conflicting source with a new
                # segment.
                if source_match_start < conflicting_sources[0].get_start():
                    new_id = self.__generate_next_id()
                    new_segment = SourceSegment.from_frequency(new_id, source_match_start,
                                                               conflicting_sources[0].get_start(), 0)
                    self.__add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                           target_match_end)
                    conflicting_sources[0].add_segment_to_start(new_segment)

                # We then need to check if the new match ends after the last conflicting source. It that is the
                # case, we need to extend the conflicting source with a new segment.
                if source_match_end > conflicting_sources[-1].get_end():
                    new_id = self.__generate_next_id()
                    new_segment = SourceSegment.from_frequency(new_id, conflicting_sources[-1].get_end(),
                                                               source_match_end, 0)
                    self.__add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                           target_match_end)
                    conflicting_sources[-1].add_segment_to_end(new_segment)

                new_source = CitationSource(conflicting_sources[0].my_id,
                                            copy.deepcopy(conflicting_sources[0].source_segments))

                # In case there is more than one conflicting source, we need to extend the new_source with the
                # existing segments and citation targets from the conflicting sources.
                for i in range(1, len(conflicting_sources)):
                    next_source = conflicting_sources[i]

                    # We need to make sure that we create a new segment which covers the gap between the
                    # current and the next source.
                    if next_source.get_start() > new_source.get_end():
                        new_id = self.__generate_next_id()
                        new_source.add_segment_to_end(SourceSegment.from_frequency(new_id, new_source.get_end(),
                                                                                   next_source.get_start(), 0))
                        self.__add_to_link_map(segment_id_to_target_location_map, new_id, filename, target_match_start,
                                               target_match_end)

                    new_source.source_segments.extend(copy.deepcopy(next_source.source_segments))

                # We now need to remove the old conflicting sources and add the newly created source
                for conflicting_position in reversed(conflicting_positions):
                    del citation_sources[conflicting_position]

                citation_sources.insert(conflicting_positions[0], new_source)

                # the last step is to update the existing segments to create non overlapping segments and adjust
                # the frequency of a segment appearing in citations.

                current_pos = source_match_start
                segments = new_source.source_segments

                while current_pos < source_match_end:
                    new_segment = None
                    new_segment_pos = -1

                    for segment_pos in range(0, len(segments)):
                        segment = segments[segment_pos]

                        if current_pos == segment.start:
                            if source_match_end < segment.end:
                                new_id = self.__generate_next_id()
                                segment_old_end = segment.end
                                segment.end = source_match_end

                                new_segment = SourceSegment.from_frequency(new_id, source_match_end,
                                                                           segment_old_end, segment.frequency)
                                segment.increment_frequency()
                                self.__copy_links(segment_id_to_target_location_map, segment.my_id, new_id)
                                self.__add_to_link_map(segment_id_to_target_location_map, segment.my_id, filename,
                                                       target_match_start, target_match_end)
                                new_segment_pos = segment_pos + 1
                                current_pos = source_match_end
                                break
                            elif source_match_end >= segment.end:
                                segment.increment_frequency()
                                self.__add_to_link_map(segment_id_to_target_location_map, segment.my_id, filename,
                                                       target_match_start, target_match_end)
                                current_pos = segment.end
                                break

                        elif segment.start < current_pos < segment.end:
                            new_id = self.__generate_next_id()
                            segment_old_end = segment.end
                            segment.end = current_pos

                            new_segment = SourceSegment.from_frequency(new_id, current_pos, segment_old_end,
                                                                       segment.frequency)
                            self.__copy_links(segment_id_to_target_location_map, segment.my_id, new_id)
                            new_segment_pos = segment_pos + 1
                            break
                        elif current_pos == segment.end:
                            if segment_pos < len(segments) - 1:
                                current_pos = segments[segment_pos + 1].start
                            else:
                                break
                        elif segment_pos == len(segments) - 1:
                            current_pos += 1

                        if current_pos >= source_match_end:
                            break

                    if new_segment:
                        segments.insert(new_segment_pos, new_segment)

        return citation_sources, segment_id_to_target_location_map

    def __add_to_link_map(self, link_map: Dict[int, List[TargetMatch]], new_id, filename: str, target_match_start: int,
                          target_match_end: int) -> None:
        if new_id in link_map:
            link_map[new_id].append(TargetMatch(filename, target_match_start, target_match_end))
        else:
            new_list = [TargetMatch(filename, target_match_start, target_match_end)]
            link_map[new_id] = new_list

    def __copy_links(self, link_map: Dict[int, List[TargetMatch]], old_id: int, new_id: int) -> None:
        link_map[new_id] = copy.deepcopy(link_map[old_id])

    def __generate_target_texts(self, texts_with_matches: List[TextWithMatches]) \
            -> (List[TargetText], Dict[int, Location]):
        target_texts = []
        target_location_id_to_source_location_map: Dict[int, Location] = {}

        for target_text_matches in texts_with_matches:
            target_text, temp_target_location_id_to_source_location_map = self.__get_target_text_from_file(
                target_text_matches)
            target_texts.append(target_text)

            target_location_id_to_source_location_map.update(temp_target_location_id_to_source_location_map)

        return target_texts, target_location_id_to_source_location_map

    def __get_target_text_from_file(self, target_text_matches: TextWithMatches) -> (TargetText, Dict[int, Location]):
        filename = target_text_matches.name
        target_content = target_text_matches.text
        target_text_id = self.__generate_next_id()
        target_locations = []
        target_location_id_to_source_location_map: Dict[int, Location] = {}

        for match in target_text_matches.matches:
            source_match_segment = match.source_match_segment
            target_match_segment = match.target_match_segment
            source_character_start_pos = source_match_segment.character_start_pos
            source_character_end_pos = source_match_segment.character_end_pos
            target_character_start_pos = target_match_segment.character_start_pos
            target_character_end_pos = target_match_segment.character_end_pos

            text = target_content[target_character_start_pos:target_character_end_pos]

            new_id = self.__generate_next_id()
            target_locations.append(TargetLocation(new_id, target_character_start_pos, target_character_end_pos, text))
            target_location_id_to_source_location_map[new_id] = Location(source_character_start_pos,
                                                                         source_character_end_pos)

        target_locations.sort(key=lambda x: x.start)

        return TargetText(target_text_id, filename, target_locations), target_location_id_to_source_location_map

    def __generate_target_text_location_links(self, citation_sources: List[CitationSource],
                                              target_texts: List[TargetText],
                                              target_location_id_to_source_location_map: Dict[int, Location]):
        target_text_location_links = []

        for target_text in target_texts:
            new_target_text_location_links = self.__generate_target_text_location_links_for_target_text(
                citation_sources,
                target_text,
                target_location_id_to_source_location_map)
            target_text_location_links.extend(new_target_text_location_links)

        return target_text_location_links

    def __generate_target_text_location_links_for_target_text(self, citation_sources: List[CitationSource],
                                                              target_text: TargetText,
                                                              target_location_id_to_source_location_map: Dict[
                                                                  int, Location]):
        target_text_location_links = []

        for target_location in target_text.target_locations:
            target_location_id = target_location.my_id
            location = target_location_id_to_source_location_map[target_location_id]

            source_segment_start_id = None
            source_segment_end_id = None

            for citation_source in citation_sources:
                for source_segment in citation_source.source_segments:
                    if source_segment.start == location.start:
                        source_segment_start_id = source_segment.my_id

                    if source_segment_start_id and source_segment.end == location.end:
                        source_segment_end_id = source_segment.my_id

                    if source_segment_start_id and source_segment_end_id:
                        break

                if source_segment_start_id and source_segment_end_id:
                    break

            if not (source_segment_start_id and source_segment_end_id):
                raise Exception('This should never happen!')  # pragma: no cover

            target_text_location_link = TargetTextLocationLink(target_text.my_id, target_location_id,
                                                               source_segment_start_id, source_segment_end_id)
            target_text_location_links.append(target_text_location_link)

        return target_text_location_links

    def __generate_citation_source_links(self, citation_sources: List[CitationSource], target_texts: List[TargetText],
                                         segment_id_to_target_matches_map: Dict[int, List[TargetMatch]]) -> \
            List[CitationSourceLink]:
        citation_source_links = []

        for citation_source in citation_sources:
            citation_source_link = \
                self.__generate_citation_source_links_for_citation_source(citation_source,
                                                                          target_texts,
                                                                          segment_id_to_target_matches_map)
            citation_source_links.append(citation_source_link)

        return citation_source_links

    def __generate_citation_source_links_for_citation_source(self, citation_source: CitationSource,
                                                             target_texts: List[TargetText],
                                                             segment_id_to_target_matches_map:
                                                             Dict[int, List[TargetMatch]]) -> CitationSourceLink:
        target_location_selections = []

        for source_segment in citation_source.source_segments:
            target_matches = segment_id_to_target_matches_map[source_segment.my_id]

            for target_match in target_matches:
                target_text_id = self.__get_target_text_id(target_match.filename, target_texts)
                existing_target_location_selection = None

                for tls in target_location_selections:
                    if tls.target_text_id == target_text_id:
                        existing_target_location_selection = tls
                        break

                if existing_target_location_selection:
                    target_location_id = self.__get_target_location_id(target_texts, target_text_id,
                                                                       target_match.start,
                                                                       target_match.end)
                    existing_target_location_selection.add_target_location_id(target_location_id)
                else:
                    target_location_id = self.__get_target_location_id(target_texts, target_text_id,
                                                                       target_match.start,
                                                                       target_match.end)
                    target_location_selection = TargetLocationSelection.from_value(target_text_id, target_location_id)
                    target_location_selections.append(target_location_selection)

        return CitationSourceLink(citation_source.my_id, target_location_selections)

    def __add_important_segments(self, citation_sources: List[CitationSource]) -> None:
        """
        Generate and add important segments for the given CitationSources.
        :param citation_sources: CitationSources for which to generate and add the important segments
        """

        pattern = re.compile("[A-Za-zäöüß]")
        # stopwords = ['der', 'die', 'das', 'daß', 'ein', 'eine', 'einer', 'eines', 'und', 'vor', 'von', 'da',
        # 'vom', 'in', 'mit', 'was', 'es', 'um', 'doch', 'auch', 'ihn']
        stopwords = []

        for citation_source in citation_sources:
            source_segment_ids = []
            last_frequency = -1
            frequency_sum = 0
            token_length = -1
            text = ''
            count = 0

            important_segments = []
            segment_pos = 0

            while segment_pos < len(citation_source.source_segments):
                segment = citation_source.source_segments[segment_pos]
                next_segment = None

                if segment_pos + 1 < len(citation_source.source_segments):
                    next_segment = citation_source.source_segments[segment_pos + 1]

                if last_frequency == -1:
                    source_segment_ids = [segment.my_id]
                    last_frequency = segment.frequency
                    frequency_sum = segment.frequency
                    token_length = segment.token_length
                    text = segment.text
                    count = 1
                    segment_pos += 1
                else:
                    diff_last = abs(last_frequency - segment.frequency)
                    diff_next = None

                    if next_segment:
                        diff_next = abs(segment.frequency - next_segment.frequency)

                    if (not diff_next or token_length <= 3 or (
                            diff_next and diff_last <= diff_next)) and diff_last <= 2:
                        source_segment_ids.append(segment.my_id)
                        frequency_sum += segment.frequency
                        token_length += segment.token_length
                        text += ' ' + segment.text
                        count += 1
                        segment_pos += 1
                    elif diff_next and diff_next < diff_last and diff_next <= 2:
                        text = re.sub(r'^[\W]+', '', text)
                        important_segments.append(ImportantSegment(self.__generate_next_id(), source_segment_ids,
                                                                   round(frequency_sum / count, 1), token_length, text))
                        source_segment_ids = [segment.my_id, next_segment.my_id]
                        last_frequency = segment.frequency
                        frequency_sum = segment.frequency + next_segment.frequency
                        token_length = segment.token_length + next_segment.token_length
                        text = segment.text + ' ' + next_segment.text
                        count = 2
                        segment_pos += 2
                    else:
                        text = re.sub(r'^[\W]+', '', text)
                        important_segments.append(ImportantSegment(self.__generate_next_id(), source_segment_ids,
                                                                   round(frequency_sum / count, 1), token_length, text))
                        source_segment_ids = [segment.my_id]
                        last_frequency = segment.frequency
                        frequency_sum = segment.frequency
                        token_length = segment.token_length
                        text = segment.text
                        count = 1
                        segment_pos += 1

            text = re.sub(r'^[\W]+', '', text)

            important_segments.append(ImportantSegment(self.__generate_next_id(), source_segment_ids,
                                                       round(frequency_sum / count, 1), token_length, text))

            important_segments.sort(key=lambda x: x.frequency, reverse=True)
            important_segments = [x for x in important_segments if x.text and pattern.search(x.text)
                                  and not x.text.lower() in stopwords]

            citation_source.important_segments = important_segments[:10]

    def __generate_important_segment_links(self, citation_sources: List[CitationSource],
                                           target_texts: List[TargetText],
                                           link_map: Dict[int, List[TargetMatch]]) -> List[ImportantSegmentLink]:
        important_segment_links = []

        for citation_source in citation_sources:
            for important_segment in citation_source.important_segments:
                target_location_selections = []

                for source_segment_id in important_segment.source_segment_ids:
                    target_matches = link_map[source_segment_id]

                    for target_match in target_matches:
                        target_text_id = self.__get_target_text_id(target_match.filename, target_texts)
                        target_location_id = self.__get_target_location_id(target_texts, target_text_id,
                                                                           target_match.start, target_match.end)

                        found = False
                        for existing_target_location_selection in target_location_selections:
                            if existing_target_location_selection.target_text_id == target_text_id:
                                existing_target_location_selection.add_target_location_id(target_location_id)
                                found = True
                                break

                        if not found:
                            target_location_selections.append(
                                TargetLocationSelection.from_value(target_text_id, target_location_id))

                important_segment_link = ImportantSegmentLink(important_segment.my_id, target_location_selections)
                important_segment_links.append(important_segment_link)

        return important_segment_links

    def __get_target_text_id(self, filename: str, target_texts: List[TargetText]) -> int:
        for target_text in target_texts:
            if target_text.filename == filename:
                return target_text.my_id

        raise Exception('This should never happen')  # pragma: no cover

    def __get_target_location_id(self, target_texts: List[TargetText], target_text_id: int,
                                 target_match_start: int, target_match_end: int) -> int:
        for target_text in target_texts:
            if target_text.my_id == target_text_id:
                for target_location in target_text.target_locations:
                    if target_location.start == target_match_start and target_location.end == target_match_end:
                        return target_location.my_id

        raise Exception('This should never happen!')  # pragma: no cover
