import warnings
from typing import List, Dict, Optional
from quid.core.InternalMatch import InternalMatch
from quid.core.BestMatch import BestMatch
from quid.core.InternalMatchSpan import InternalMatchSpan
from quid.match.Match import Match
from quid.match.MatchSpan import MatchSpan
from quid.core.Text import Text
import re
from quid.core.Token import Token
from rapidfuzz import fuzz, process
from datasketch import MinHash, MinHashLSH


# noinspection PyMethodMayBeStatic
# This algorithm is based on the algorithm by Dick Grune, see https://dickgrune.com/Programs/similarity_tester/.
# And a Javascript implementation, see
# https://people.f4.htw-berlin.de/~weberwu/simtexter/522789_Sofia-Kalaidopoulou_bachelor-thesis.pdf
class Quid:
    tokens: List[Token]
    texts: List[Text]
    forward_references: Dict[int, List[int]]
    # Values relevant for fuzzy matching
    HASH_PERM: int = 128
    SCORE_CUTOFF_SHORT_STRINGS: int = 85
    SCORE_CUTOFF: int = 90
    LSH_THRESHOLD: float = 0.95

    SENTENCE_DELIMITER = '\u03B1'
    SENTENCE_DELIMITER_START_REGEX: str = f'^[{SENTENCE_DELIMITER}]'
    SENTENCE_DELIMITER_END_REGEX: str = f'[{SENTENCE_DELIMITER}]$'

    def __init__(self, min_match_length: int = 5,
                 look_back_limit: int = 10,
                 look_ahead_limit: int = 3,
                 max_merge_distance: int = 2,
                 max_merge_ellipse_distance: int = 10,
                 include_text_in_result: bool = True,
                 keep_ambiguous_matches: bool = False):

        """
        :param min_match_length: The length of the shortest match
        :param look_back_limit: The number of tokens to skip when looking backwards
        :param look_ahead_limit: The number of tokens to skip when looking ahead
        :param max_merge_distance: The maximum distance in tokens between to matches considered for merging
        :param max_merge_ellipse_distance: The maximum distance in tokens between two matches considered for merging
        where the target text contains an ellipses between the matches
        """

        if min_match_length < 1:
            raise ValueError('min match length must be >= 1')

        if min_match_length < 3:
            warnings.warn('A small minimal match length can lead to long processing times '
                          '(recommendation: min_match_length >= 3)')

        if look_back_limit < 0:
            raise ValueError('look back limit must be positive')

        if look_ahead_limit < 0:
            raise ValueError('look ahead limit must be positive')

        if max_merge_distance < 0:
            raise ValueError('max merge distance must be positive')

        if max_merge_ellipse_distance < 0:
            raise ValueError('max merge ellipse distance must be positive')

        self.initial_match_length = min(3, min_match_length)
        self.min_match_length = min_match_length
        self.look_back_limit = look_back_limit
        self.look_ahead_limit = look_ahead_limit
        self.max_merge_distance = max_merge_distance
        self.max_merge_ellipse_distance = max_merge_ellipse_distance
        self.forward_references = {}
        self.texts = []
        self.tokens = []
        self.include_text_in_result = include_text_in_result
        self.keep_ambiguous_matches = keep_ambiguous_matches

    def compare(self, source_text: str, target_text: str) -> List[Match]:
        """
        Compare the two input texts and return a list of matching sequences.
        :param source_text: A source text
        :param target_text: A target text
        :return: A list of found matches
        """

        if not source_text or not target_text:
            return []

        input_texts: List[str] = [source_text, target_text]
        self.texts, self.tokens = self.__read_input(input_texts)
        self.forward_references = {}

        min_length_match_positions: Dict[str, List[int]]
        hashes: MinHashLSH
        min_length_match_positions, hashes = self.__make_min_length_match_starting_positions(self.texts[0])
        self.__make_forward_references(self.texts[1], min_length_match_positions, hashes)
        matches: List[InternalMatch] = self.__get_similarities(self.texts[0], self.texts[1])
        matches.sort(key=lambda x: x.target_match_span.character_start, reverse=False)

        # self.__print_matches(matches, source_text, target_text)

        cleaned_matches: List[InternalMatch] = self.__merge_neighbouring_matches(matches)
        cleaned_matches = self.__remove_matches_with_overlapping_target_match_spans(cleaned_matches)
        cleaned_matches = self.__remove_too_short_matches(cleaned_matches)
        self.__remove_boundary_overshoot(cleaned_matches)

        # self.__print_matches(cleaned_matches, source_text, target_text)

        result: List[Match] = []
        for internal_match in cleaned_matches:
            source_match_span = MatchSpan(internal_match.source_match_span.character_start,
                                          internal_match.source_match_span.character_end)
            target_match_span = MatchSpan(internal_match.target_match_span.character_start,
                                          internal_match.target_match_span.character_end)

            if self.include_text_in_result:
                segment_source_text = source_text[source_match_span.start:
                                                  source_match_span.end]
                segment_target_text = target_text[target_match_span.start:
                                                  target_match_span.end]

                source_match_span.text = segment_source_text
                target_match_span.text = segment_target_text

            result.append(Match(source_match_span, target_match_span))

        return result

    def __read_input(self, input_texts: List[str]) -> (List[Text], List[Token]):
        texts: List[Text] = []
        tokens: List[Token] = []

        for input_text in input_texts:
            nr_of_characters = len(input_text)
            nr_of_words = len(input_text.split())
            tk_start_pos = len(tokens)

            tokens.extend(self.__tokenize_text(input_text))
            tk_end_pos = len(tokens)
            text = Text(nr_of_characters, nr_of_words, tk_start_pos, tk_end_pos)
            texts.append(text)

        return texts, tokens

    def __tokenize_text(self, input_text: str) -> List[Token]:
        cleaned_text = self.__clean_text(input_text)
        tokens = []

        for match in re.finditer(r'\S+', cleaned_text):
            token = self.__clean_word(match.group())

            if len(token) > 0:
                text_begin_pos = match.start()
                text_end_pos = match.end()
                tokens.append(Token(token, text_begin_pos, text_end_pos))

        return tokens

    def __clean_text(self, input_text: str) -> str:
        input_text = re.sub('(\\[\\.\\.\\.]|\\[…]|\\.\\.\\.|…)', lambda x: '@' * len(x.group(1)), input_text)
        input_text = re.sub('[.;!?]', self.SENTENCE_DELIMITER, input_text)
        input_text = re.sub(f'[^a-zA-Z\\däüöÄÜÖß@{self.SENTENCE_DELIMITER} ]', ' ', input_text)
        input_text = re.sub(r'\d', ' ', input_text)
        return input_text.lower()

    def __clean_word(self, input_word: str) -> str:
        input_word = input_word.replace('ß', 'ss')
        input_word = input_word.replace('ä', 'ae')
        input_word = input_word.replace('ö', 'oe')
        input_word = input_word.replace('ü', 'ue')
        input_word = input_word.replace('ey', 'ei')
        return input_word

    def __remove_special_characters(self, input_string: str) -> str:

        input_string = re.sub(r'[^a-zA-Z\däüöÄÜÖß@ ]', '', input_string)

        if re.search(r'[a-zA-Z\däüöÄÜÖß]', input_string):
            input_string = re.sub('@', '', input_string)

        return input_string

    def __make_min_length_match_starting_positions(self, text: Text) -> (Dict[str, List[int]], MinHashLSH):
        """
        Takes a source text and returns a tuple consisting of a map and a list of hashes. The map maps strings to their
        starting positions in the text.
        :param text: The source text
        :return: A tuple consisting of a map of strings and their starting positions and a list of hashes of the strings
        in the map.
        """

        min_length_match_starting_positions: Dict[str, List[int]] = {}
        hashes: MinHashLSH = MinHashLSH(threshold=self.LSH_THRESHOLD, num_perm=self.HASH_PERM)

        text_begin_pos: int = text.tk_start_pos
        text_end_pos: int = text.tk_end_pos

        for position in range(text_begin_pos, text_end_pos - self.initial_match_length + 1):
            minimal_match_string: str = ''

            for token in self.tokens[position: position + self.initial_match_length]:
                minimal_match_string += token.text

            minimal_match_string = self.__remove_special_characters(minimal_match_string)
            minimal_match_character_set = set(minimal_match_string)
            minimal_match_hash = MinHash(num_perm=self.HASH_PERM)

            for char in minimal_match_character_set:
                minimal_match_hash.update(char.encode('utf8'))

            hashes.insert(minimal_match_string, minimal_match_hash, False)

            if minimal_match_string in min_length_match_starting_positions:
                min_length_match_starting_positions[minimal_match_string].append(position)
            else:
                min_length_match_starting_positions[minimal_match_string] = [position]

        return min_length_match_starting_positions, hashes

    def __make_forward_references(self, text: Text, min_length_match_starting_positions: Dict[str, List[int]],
                                  hashes: MinHashLSH):
        """
        Takes a target text, a mapping of strings to the position in the source text where a string starts
        and a list of hashes.
        It then tries to find matching strings in the target texts and creates a mapping of the starting positions in
        the source text to a list of starting positions in the target text.
        :param text: The target text
        :param min_length_match_starting_positions: A map of strings to positions where the string is a combination of
        x tokens.
        mapped to the position in the text where the string starts.
        :param hashes: The hashes of the minimal length strings.
        :return: A mapping of starting positions in the source text to a list of starting positions in the target text.
        """

        text_begin_pos: int = text.tk_start_pos
        text_end_pos: int = text.tk_end_pos

        for token_pos in range(text_begin_pos, text_end_pos - self.initial_match_length + 1):
            minimal_match_string: str = ''

            for token in self.tokens[token_pos: token_pos + self.initial_match_length]:
                minimal_match_string += self.__remove_special_characters(token.text)

            minimal_match_character_set = set(minimal_match_string)
            minimal_match_hash = MinHash(num_perm=self.HASH_PERM)

            for char in minimal_match_character_set:
                minimal_match_hash.update(char.encode('utf8'))

            possible_matches = hashes.query(minimal_match_hash)

            closest_match = self.__get_closest_match(possible_matches, minimal_match_string)
            if closest_match:
                for match_starting_position in min_length_match_starting_positions[closest_match]:
                    if match_starting_position in self.forward_references:
                        self.forward_references[match_starting_position].append(token_pos)
                    else:
                        self.forward_references[match_starting_position] = [token_pos]

    def __get_similarities(self, source_text: Text, target_text: Text) -> List[InternalMatch]:
        """
        Takes a source text and a target text and tries to find matching sequences.
        :param source_text: The source text
        :param target_text: The target text
        :return: A list of matches.
        """

        target_position_to_source_positions_map = {}

        for source_token_position, target_token_positions in self.forward_references.items():
            for target_token_position in target_token_positions:
                if target_token_position in target_position_to_source_positions_map:
                    target_position_to_source_positions_map[target_token_position].append(source_token_position)
                else:
                    target_position_to_source_positions_map[target_token_position] = [source_token_position]

        source_token_start_pos = source_text.tk_start_pos
        source_token_end_pos = source_text.tk_end_pos
        matches: List[InternalMatch] = []

        while source_token_start_pos + self.initial_match_length <= source_token_end_pos:
            best_match: Optional[BestMatch] = self.__get_best_match(source_text, target_text,
                                                                    source_token_start_pos)

            if best_match and best_match.source_length > 0:
                source_character_start_pos = self.tokens[best_match.source_token_start].start_pos
                source_character_end_pos = self.tokens[
                    best_match.source_token_start + best_match.source_length - 1].end_pos
                target_character_start_pos = self.tokens[best_match.target_token_start].start_pos
                target_character_end_pos = self.tokens[
                    best_match.target_token_start + best_match.target_length - 1].end_pos

                source_match_span = InternalMatchSpan(best_match.source_token_start, best_match.source_length,
                                                      source_character_start_pos, source_character_end_pos)
                target_match_span = InternalMatchSpan(best_match.target_token_start, best_match.target_length,
                                                      target_character_start_pos, target_character_end_pos)

                matches.append(InternalMatch(source_match_span, target_match_span))

                best_match_token_start_pos = best_match.target_token_start
                best_match_token_end_pos = best_match.target_token_start + best_match.target_length

                best_match_source_token_start_pos = best_match.source_token_start
                best_match_source_token_end_pos = best_match.source_token_start + best_match.source_length

                for target_token_pos in range(best_match_token_start_pos + 1, best_match_token_end_pos):
                    if target_token_pos in target_position_to_source_positions_map:
                        for source_token_position in target_position_to_source_positions_map[target_token_pos]:
                            if best_match_source_token_start_pos < source_token_position < best_match_source_token_end_pos:
                                if target_token_pos in self.forward_references[source_token_position]:
                                    self.forward_references[source_token_position].remove(target_token_pos)
            else:
                if source_token_start_pos not in self.forward_references.keys() or len(
                        self.forward_references[source_token_start_pos]) == 0:
                    source_token_start_pos += 1

        return matches

    def __get_best_match(self, source_text: Text, target_text: Text, source_token_start_pos: int) \
            -> Optional[BestMatch]:
        """
        Find the next best match starting from the given position.
        :param source_text: The source text
        :param target_text: The target text
        :param source_token_start_pos: The position from which to start looking
        :return: The best match or None if no match was found
        """

        target_token_start_pos = self.__get_next_target_token_position(source_token_start_pos)

        if target_token_start_pos == -1:
            return None

        best_match = None
        offset_source = 0
        offset_target = 0

        min_match_length = self.initial_match_length

        # find possibly better start point
        new_source_token_start = source_token_start_pos
        new_target_token_start = target_token_start_pos
        source_extra_length = 0
        target_extra_length = 0

        if self.tokens[new_target_token_start - 1].text.startswith('@'):
            for i in range(1, min(self.look_back_limit, new_source_token_start)):
                if self.__fuzzy_match(self.tokens[new_source_token_start - i].text,
                                      self.tokens[new_target_token_start - 2].text):
                    new_source_token_start -= i
                    new_target_token_start -= 2
                    source_extra_length += i
                    target_extra_length += 2

                    for j in range(1, min(self.initial_match_length - 1, new_source_token_start + 1)):
                        if self.__fuzzy_match(self.tokens[new_source_token_start - j].text,
                                              self.tokens[new_target_token_start - j].text):
                            new_source_token_start -= 1
                            new_target_token_start -= 1
                            source_extra_length += 1
                            target_extra_length += 1

                    break

        new_match_length = min_match_length
        source_token_pos = source_token_start_pos + min_match_length
        target_token_pos = target_token_start_pos + min_match_length

        has_skipped = False

        while source_token_pos < source_text.tk_end_pos and target_text.tk_end_pos > target_token_pos:

            # skip from 1 to n tokens in source text. N can be defined by the user.
            if self.tokens[target_token_pos].text.startswith('@'):
                found = False

                for i in range(1, self.look_ahead_limit + 1):
                    if (target_token_pos + 1 < len(self.tokens) and source_token_pos + i < source_text.tk_end_pos and
                            self.__fuzzy_match(self.tokens[source_token_pos + i].text,
                                               self.tokens[target_token_pos + 1].text)):
                        source_token_pos += i
                        target_token_pos += 1
                        new_match_length += i
                        offset_target += i - 1
                        found = True
                        break

                if not found:
                    break

            # do tokens at aligned positions match
            if self.__fuzzy_match(self.tokens[source_token_pos].text, self.tokens[target_token_pos].text):
                source_token_pos += 1
                target_token_pos += 1
                new_match_length += 1
            # combine two tokens in source text
            elif (source_token_pos + 1 < source_text.tk_end_pos and
                  self.__fuzzy_match(self.tokens[source_token_pos].text + self.tokens[source_token_pos + 1].text,
                                     self.tokens[target_token_pos].text)):
                source_token_pos += 2
                target_token_pos += 1
                new_match_length += 2
                offset_target += 1
            # combine two tokens in target text
            elif (target_token_pos + 1 < len(self.tokens) and
                  self.__fuzzy_match(self.tokens[source_token_pos].text,
                                     self.tokens[target_token_pos].text +
                                     self.tokens[target_token_pos + 1].text)):
                source_token_pos += 1
                target_token_pos += 2
                new_match_length += 2
                offset_source += 1
            elif not has_skipped:
                found = False

                # skip one token in the source text
                if (source_token_pos + 1 < source_text.tk_end_pos and
                        self.__fuzzy_match(self.tokens[source_token_pos + 1].text, self.tokens[target_token_pos].text)):
                    source_token_pos += 2
                    target_token_pos += 1
                    new_match_length += 2
                    offset_target += 1
                    found = True
                    has_skipped = True

                if not found:
                    # skip one token in the target text
                    if (target_token_pos + 1 < len(self.tokens) and
                            self.__fuzzy_match(self.tokens[source_token_pos].text,
                                               self.tokens[target_token_pos + 1].text)):
                        source_token_pos += 1
                        target_token_pos += 2
                        new_match_length += 2
                        offset_source += 1
                        found = True
                        has_skipped = True

                if not found:
                    break
            else:
                break

        if new_match_length >= self.initial_match_length:
            best_match_token_pos = target_token_start_pos
            best_match = BestMatch(source_token_start_pos - source_extra_length,
                                   best_match_token_pos - target_extra_length,
                                   new_match_length - offset_source + source_extra_length,
                                   new_match_length - offset_target + target_extra_length)

        return best_match

    def __get_next_target_token_position(self, current_source_token_position: int) -> int:
        """
        Takes a source token position and gets the next target token position if possible.
        :param current_source_token_position: A source token position
        :return: The next target token position or -1 if no position could be found.
        """

        for source_token_position, target_token_positions in self.forward_references.items():
            if current_source_token_position == source_token_position and len(target_token_positions) > 0:
                next_token_position = target_token_positions[0]
                del target_token_positions[0]
                return next_token_position

        return -1

    def __fuzzy_match(self, input1: str, input2: str) -> bool:
        input1 = self.__remove_special_characters(input1)
        input2 = self.__remove_special_characters(input2)

        input1_length = len(input1)
        input2_length = len(input2)

        if min(input1_length, input2_length) < 2:
            return input1 == input2

        ratio = fuzz.ratio(input1, input2)

        if max(input1_length, input2_length) < 10:
            return ratio >= self.SCORE_CUTOFF_SHORT_STRINGS

        return ratio >= self.SCORE_CUTOFF

    def __get_closest_match(self, candidates: List[str], word: str) -> Optional[str]:
        if not candidates or len(candidates) == 0:
            return None

        candidates = [self.__remove_special_characters(element) for element in candidates]
        word = self.__remove_special_characters(word)

        if word in candidates:
            return word

        best_candidate = process.extractOne(word, candidates, scorer=fuzz.ratio, score_cutoff=self.SCORE_CUTOFF)

        if best_candidate:
            return best_candidate[0]

        return None

    def __remove_matches_with_overlapping_target_match_spans(self, matches: List[InternalMatch]):
        """
        Removes matches which overlap in the target texts. When keep_ambiguous_matches is true, then matches are only
        removed if they also overlap in the source text.
        @param matches: The input list of matches.
        @return: The remaining matches.
        """
        if len(matches) == 0:
            return []

        result: List[InternalMatch] = []

        if not self.keep_ambiguous_matches:
            match_position: int = 1
            current_match = matches[0]

            while match_position < len(matches):
                next_match = matches[match_position]

                current_target_match_span = current_match.target_match_span
                next_target_match_span = next_match.target_match_span

                current_end_pos = current_target_match_span.character_end
                next_start_pos = next_target_match_span.character_start

                if next_start_pos >= current_end_pos:
                    result.append(current_match)
                    current_match = next_match
                else:
                    current_token_length = current_target_match_span.token_length
                    next_token_length = next_target_match_span.token_length

                    if current_token_length < next_token_length:
                        current_match = next_match

                match_position += 1

            result.append(current_match)
        else:
            for current_match_pos, current_match in enumerate(matches):
                found_conflict = False
                for next_match_pos in range(current_match_pos, len(matches)):
                    next_match = matches[next_match_pos]

                    current_target_match_span = current_match.target_match_span
                    next_target_match_span = next_match.target_match_span

                    current_end_pos = current_target_match_span.character_end
                    next_start_pos = next_target_match_span.character_start

                    if next_start_pos < current_end_pos:
                        source_current_start_pos = current_match.source_match_span.character_start
                        source_current_end_pos = current_match.source_match_span.character_end
                        source_next_start_pos = next_match.source_match_span.character_end
                        source_next_end_pos = next_match.source_match_span.character_end

                        overlap_start = max(source_current_start_pos, source_next_start_pos)
                        overlap_end = min(source_current_end_pos, source_next_end_pos)
                        overlap_length = overlap_end - overlap_start

                        if overlap_length > 0:
                            current_token_length = current_target_match_span.token_length
                            next_token_length = next_target_match_span.token_length

                            if current_token_length < next_token_length:
                                found_conflict = True
                                break
                    else:
                        break

                if not found_conflict:
                    result.append(current_match)

        return result

    def __merge_neighbouring_matches(self, matches: List[InternalMatch]):
        """
        Merges matches which are closer together than the defined threshold.
        :param matches: The input list of matches.
        :return: The new list of matches.
        """

        remaining_matches = matches
        result = []

        while len(remaining_matches) > 0:
            current_match = remaining_matches[0]
            positions_to_delete = [0]

            for i in range(1, len(remaining_matches)):
                next_match = remaining_matches[i]

                current_source_sim = current_match.source_match_span
                next_source_sim = next_match.source_match_span
                current_target_sim = current_match.target_match_span
                next_target_sim = next_match.target_match_span

                current_source_start = current_source_sim.token_start_pos
                current_target_start = current_target_sim.token_start_pos
                next_source_start = next_source_sim.token_start_pos
                next_target_start = next_target_sim.token_start_pos
                current_source_end = current_source_sim.token_start_pos + current_source_sim.token_length
                current_target_end = current_target_sim.token_start_pos + current_target_sim.token_length
                next_source_end = next_source_sim.token_start_pos + next_source_sim.token_length
                next_target_end = next_target_sim.token_start_pos + next_target_sim.token_length

                if ((0 <= next_target_start - current_target_end <= self.max_merge_distance
                     and 0 <= next_source_start - current_source_end <= self.max_merge_distance)
                        or (next_target_start - current_target_end == 1
                            and self.tokens[next_target_start - 1].text.startswith('@')
                            and current_source_start < next_source_start
                            and next_source_start - current_source_end <= self.max_merge_ellipse_distance)
                        or (next_target_end > current_target_end > next_target_start > current_target_start
                            and next_source_end > current_source_end > next_source_start > current_source_start)):

                    source_match_span = InternalMatchSpan(current_source_sim.token_start_pos,
                                                          next_source_sim.token_start_pos +
                                                          next_source_sim.token_length -
                                                          current_source_sim.token_start_pos,
                                                          current_source_sim.character_start,
                                                          next_source_sim.character_end)

                    target_match_span = InternalMatchSpan(current_target_sim.token_start_pos,
                                                          next_target_sim.token_start_pos +
                                                          next_target_sim.token_length -
                                                          current_target_sim.token_start_pos,
                                                          current_target_sim.character_start,
                                                          next_target_sim.character_end)
                    current_match = InternalMatch(source_match_span, target_match_span)

                    positions_to_delete.append(i)
                elif 0 <= next_target_start - current_target_end > self.max_merge_distance:
                    break

            for position in reversed(positions_to_delete):
                del remaining_matches[position]

            result.append(current_match)

        return result

    def __remove_too_short_matches(self, matches: List[InternalMatch]):
        """
        Removes matches which are shorter than a threshold.
        @param matches: The list of matches to check.
        @return: The remaining matches.
        """
        result: List[InternalMatch] = []

        for match in matches:
            if match.target_match_span.token_length >= self.min_match_length:
                result.append(match)
            elif (match.target_match_span.token_length >= self.min_match_length - 1 and
                  self.tokens[match.target_match_span.token_start_pos].text.startswith('@')):
                result.append(match)
            elif (match.target_match_span.token_length >= self.min_match_length - 1 and
                  match.target_match_span.token_start_pos - 1 >= self.texts[0].tk_end_pos and
                  (self.tokens[match.target_match_span.token_start_pos].text.startswith('@') or
                   self.tokens[match.target_match_span.token_start_pos - 1].text.startswith('@'))):
                result.append(match)

        return result

    def __remove_boundary_overshoot(self, matches: List[InternalMatch]):
        """
        Remove tokens after sentence delimiters if they're likely to have matched by accident.
        @param matches: The list of matches to check.
        @return: The cleaned matches.
        """
        for match in matches:
            current_source_match_span = match.source_match_span
            current_target_match_span = match.target_match_span

            found = False
            if current_source_match_span.token_length > 3:
                source_token_end_pos = current_source_match_span.token_start_pos + \
                                       current_source_match_span.token_length
                source_token_text = self.tokens[source_token_end_pos - 1].text

                target_token_end_pos = (current_target_match_span.token_start_pos +
                                        current_target_match_span.token_length)

                target_token_text = self.tokens[target_token_end_pos - 1].text

                if (re.search(self.SENTENCE_DELIMITER_START_REGEX, source_token_text) or
                        re.search(self.SENTENCE_DELIMITER_END_REGEX, source_token_text) or
                        re.search(self.SENTENCE_DELIMITER_START_REGEX, target_token_text) or
                        re.search(self.SENTENCE_DELIMITER_END_REGEX, target_token_text)):
                    continue

                for i in range(2, 4):
                    source_token = self.tokens[source_token_end_pos - i]
                    source_token_text = source_token.text

                    if (re.search(self.SENTENCE_DELIMITER_START_REGEX, source_token_text) or
                            re.search(self.SENTENCE_DELIMITER_END_REGEX, source_token_text)):

                        for j in range(2, 4):
                            target_token = self.tokens[target_token_end_pos - j]
                            target_token_text = target_token.text

                            if target_token_text in source_token_text:
                                found = True

                                current_source_match_span.token_length -= i
                                current_target_match_span.token_length -= j

                                current_source_match_span.character_end = self.tokens[
                                    source_token_end_pos - i].end_pos
                                current_target_match_span.character_end = self.tokens[
                                    target_token_end_pos - j].end_pos
                                break

                        if found:
                            break

    def __print_matches(self, matches, literature_content, scientific_content):  # pragma: no cover

        result = ''

        for match in matches:
            similarity_literature = match.source_span
            similarity_scientific = match.target_span

            content = literature_content[
                      similarity_literature.start:similarity_literature.end]
            result += f'\n\n{similarity_literature.start}\t{similarity_literature.end}' \
                      f'\t{content}'

            content = scientific_content[
                      similarity_scientific.start:similarity_scientific.end]
            result += f'\n{similarity_scientific.start}\t{similarity_scientific.end}' \
                      f'\t{content}'

        print(result)
