from quid.passager.CitationSource import CitationSource
from quid.passager.CitationSourceLink import CitationSourceLink
from quid.passager.SourceSegment import SourceSegment
from quid.passager.TargetLocationSelection import TargetLocationSelection
from quid.passager.TargetTextLocationLink import TargetTextLocationLink
from quid.match.Match import Match
from quid.match.MatchSpan import MatchSpan


def json_decoder_match(json_input):
    if 'source_span' in json_input and 'target_span' in json_input:
        return Match(json_input['source_span'], json_input['target_span'])
    else:
        return MatchSpan(json_input['start'], json_input['end'])


def json_decoder_citation_source(json_input):
    if 'source_segments' in json_input:
        return CitationSource(json_input['my_id'], json_input['source_segments'], json_input['text'])
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
