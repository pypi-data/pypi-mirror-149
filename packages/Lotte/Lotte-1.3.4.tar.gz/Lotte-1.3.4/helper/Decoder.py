from key_passager.CitationSource import CitationSource
from key_passager.CitationSourceLink import CitationSourceLink
from key_passager.ImportantSegment import ImportantSegment
from key_passager.SourceSegment import SourceSegment
from key_passager.TargetLocationSelection import TargetLocationSelection
from key_passager.TargetTextLocationLink import TargetTextLocationLink
from match.Match import Match
from match.MatchSegment import MatchSegment


def json_decoder_match(json_input):
    if 'source_match_segment' in json_input and 'target_match_segment' in json_input:
        return Match(json_input['source_match_segment'], json_input['target_match_segment'])
    else:
        return MatchSegment(json_input['character_start_pos'], json_input['character_end_pos'])


def json_decoder_citation_source(json_input):
    if 'source_segments' in json_input:
        return CitationSource(json_input['my_id'], json_input['source_segments'], json_input['important_segments'],
                              json_input['text'])
    elif 'source_segment_ids' in json_input:
        return ImportantSegment(json_input['my_id'], json_input['source_segment_ids'], json_input['frequency'],
                                json_input['token_length'], json_input['text'])
    else:
        return SourceSegment(json_input['my_id'], json_input['start'], json_input['end'], json_input['frequency'],
                             json_input['token_length'], '')


def json_decoder_target_text_location_link(json_input):
    return TargetTextLocationLink(json_input['target_text_id'], json_input['location_id'],
                                  json_input['source_segment_start_id'], json_input['source_segment_end_id'])


def json_decoder_citation_source_link(json_input):
    if 'citation_source_id' in json_input:
        return CitationSourceLink(json_input['citation_source_id'], json_input['target_location_selections'])
    elif 'target_text_id' in json_input:
        return TargetLocationSelection(json_input['target_text_id'], json_input['target_location_ids'])
