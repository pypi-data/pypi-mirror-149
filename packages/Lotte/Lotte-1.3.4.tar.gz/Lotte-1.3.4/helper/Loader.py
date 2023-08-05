import json
from helper.Decoder import json_decoder_match, json_decoder_citation_source, json_decoder_target_text_location_link, \
    json_decoder_citation_source_link


def load_matches(input_path):
    with open(input_path, 'r', encoding='utf-8') as matches_file:
        matches = json.load(matches_file, object_hook=json_decoder_match)
        return matches


def load_citation_sources(input_path):
    with open(input_path, 'r', encoding='utf-8') as citation_sources_file:
        citation_sources = json.load(citation_sources_file, object_hook=json_decoder_citation_source)
        return citation_sources


def load_target_text_location_links(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        target_text_location_links = json.load(file, object_hook=json_decoder_target_text_location_link)
        return target_text_location_links


def load_citation_source_links(input_path):
    with open(input_path, 'r', encoding='utf-8') as citation_source_links_file:
        citation_source_links = json.load(citation_source_links_file, object_hook=json_decoder_citation_source_link)
        return citation_source_links
