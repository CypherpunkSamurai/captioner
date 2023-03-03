import csv
import logging
from typing import Tuple, List
from fast_autocomplete.misc import read_csv_gen
from fast_autocomplete import AutoComplete


class FastAutocompleteEngine(object):
    is_working: bool = False

    def __init__(self, completer_file: str):
        """
        init a new FastAutocompleter with a completer_file (list of words)
        """

        # read file
        self.__read_wordlist_from(completer_file)
        logging.info(f"FastAutoComplete ok. {len(self.words)} words available")
        self.is_working = True

        # init
        self.fast_autocomplete = AutoComplete(words=self.words)

    def __read_wordlist_from(self, word_file: str) -> any:
        # read
        self.words = {}
        
        # add
        with open(word_file, 'r',  errors='ignore', encoding='utf-8') as file:
            lines = file.readlines()
            for w in lines:
                self.words[w.strip()] = {}
        
        return self.words

    def complete(self, completion_prefix: str, max_cost: int = 1, n: int = 6):
        """
        provide completion for the completion prefix

        :param completion_prefix: the prefix of the word to be completed
        :param max_cost: the max cost to complete the word
        :param n: the number of result
        :return:
        """

        # complete the word
        r = self.fast_autocomplete.search(completion_prefix, size=n, max_cost=max_cost)

        words: List[str] = []
        for w in r: words.append(' '.join(w))

        return words
