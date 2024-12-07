from better_profanity import Profanity

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], 'censor'))
from ban_words import BAN_WORDS
from constants import ALLOWED_CHARACTERS
 
class Censor(Profanity):
    '''
    
    '''
    def hide_swear_words(self, text, censor_char):
        """Replace the swear words with censor characters."""
        censored_text = ""
        cur_word = ""
        skip_index = -1
        next_words_indices = []
        start_idx_of_next_word = self._get_start_index_of_next_word(text, 0)

        # If there are no words in the text, return the raw text without parsing
        if start_idx_of_next_word >= len(text) - 1:
            return text

        # Left strip the text, to avoid inaccurate parsing
        if start_idx_of_next_word > 0:
            censored_text = text[:start_idx_of_next_word]
            text = text[start_idx_of_next_word:]

        # Splitting each word in the text to compare with censored words
        # print(text)
        for index, char in iter(enumerate(text)):
            if index < skip_index:
                continue
            if char in ALLOWED_CHARACTERS:
                cur_word += char
                continue

            # Skip continuous non-allowed characters
            if cur_word.strip() == "":
                censored_text += char
                cur_word = ""
                continue

            # Iterate the next words combined with the current one
            # to check if it forms a swear word
            next_words_indices = self._update_next_words_indices(
                text, next_words_indices, index
            )
            contains_swear_word, end_index = any_next_words_form_swear_word(
                cur_word, next_words_indices, self.CENSOR_WORDSET
            )
            # print(contains_swear_word)
            if contains_swear_word:
                cur_word = get_replacement_for_swear_word(cur_word, censor_char)
                skip_index = end_index
                char = ""
                next_words_indices = []

            # If the current a swear word
            if cur_word.lower() in self.CENSOR_WORDSET:
                cur_word = get_replacement_for_swear_word(cur_word, censor_char)
                # print(cur_word)
            censored_text += cur_word + char
            cur_word = ""

        # Final check
        if cur_word != "" and skip_index < len(text) - 1:
            if cur_word.lower() in self.CENSOR_WORDSET:
                cur_word = get_replacement_for_swear_word(cur_word, censor_char)
            censored_text += cur_word
        return censored_text


def get_complete_path_of_file(filename):
    """Join the path of the current directory with the input filename."""
    root = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(root, filename)


def read_wordlist(filename: str):
    """Return words from a wordlist file."""
    with open(filename, encoding="utf-8") as wordlist_file:
        for row in iter(wordlist_file):
            row = row.strip()
            if row != "":
                yield row


def get_replacement_for_swear_word(cur_word, censor_char):
    return cur_word[0] + (censor_char * (len(cur_word) - 1))


def any_next_words_form_swear_word(cur_word, words_indices, censor_words):
    """
    Return True, and the end index of the word in the text,
    if any word formed in words_indices is in `CENSOR_WORDSET`.
    """
    full_word = cur_word.lower()
    full_word_with_separators = cur_word.lower()

    # Check both words in the pairs
    for index in iter(range(0, len(words_indices), 2)):
        single_word, end_index = words_indices[index]
        word_with_separators, _ = words_indices[index + 1]
        if single_word == "":
            continue

        full_word = "%s%s" % (full_word, single_word.lower())
        full_word_with_separators = "%s%s" % (
            full_word_with_separators,
            word_with_separators.lower(),
        )
        if full_word in censor_words or full_word_with_separators in censor_words:
            return True, end_index
    return False, -1