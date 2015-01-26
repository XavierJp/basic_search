# -*- coding: utf-8 -*-

# Imports
# -------
from math import log10
from Config import Config
from collections import defaultdict
import re

import operator

# Class
# ------------------------------


class Index:
    """
    Represent an Index

    """

    def __init__(self):
        self.my_config = Config()
        self.reversed_index = {}
        self.my_dict = {}
        self.index = {}
        self.load_file(self.my_config.path)
        self.N = len(self.my_dict.keys())

    def __str__(self):
        return reversed_index

    def load_file(self, path):
        lines = self.open_file(path)
        self.make_index(lines)

    def open_file(self, path):
        f = open(path, 'r')
        data = f.read().splitlines()
        f.close()
        return data

    def make_index(self, lines):
        """ convert raw doc into an index of words and docIDs """
        doc_id = ''
        doc_mark = ''
        for i, l in enumerate(lines):
            if l[:3] == '.I ':
                doc_id = l[3:]
                doc_mark = '.I '
                self.my_dict[doc_id] = defaultdict(str)
            else:
                if l[:2] in self.my_config.k_word:
                    doc_mark = l[:2]
                else:
                    if doc_mark in self.my_config.used_k_word:
                        self.tokenize(l, doc_id)
                        self.my_dict[doc_id][doc_mark] += l

    def tokenize(self, string, doc_id):
        """ convert a string into a tokenized string (indexed) """
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+", string)
        for word in wordsBuffer:
            word = word.lower()
            if not self.compare(word):
                # populate doc_index
                self.populate_index(self.reversed_index, word, doc_id, True)
                self.populate_index(self.index, doc_id, word, False)

    def populate_index(self, index, k1, k2, compute_df):
        """ 
            generic function to create index.
            Index and reversed index have the same structure
        """
        if k1 not in index:
            index[k1] = defaultdict(int)
            if not compute_df:
                index[k1]['w_max'] = 0
        index[k1][k2] += 1
        if not compute_df:
            if index[k1][k2] > index[k1]['w_max']:
                index[k1]['w_max'] = index[k1][k2]

    def compare(self, element):
        """ 
            test if a word belong to common words list.
            If so let's remove it (not relevant)!
        """
        if element in self.my_config.words:
            return True
        return False

    def get_title_by_doc_id(self, doc_id, k_words):
        """ 
            from a docID returns corresponding element
            (example: '.T' is for title)
        """
        if doc_id in self.my_dict.keys():
            for k in k_words:
                if k in self.my_dict[doc_id]:
                    return self.my_dict[doc_id][k]
        return "Sorry, there is no document: "+str(doc_id)

    def search_a_doc_id(self, doc_id):
        """ returns results for a given docID """
        try:
            boolean = int(doc_id)
        except ValueError:
            return "\n /!\ Doc_id must be a number ! \n"

        if boolean:
            if doc_id in self.my_dict.keys():
                return str(doc_id)+': '+self.get_title_by_doc_id(doc_id, ['.T'])+'\n'
            else:
                return "Sorry, there is no document: "+str(doc_id)

    def search_a_word(self, input_word):
        """ returns a list of doc_id where word occurs """
        if input_word in self.reversed_index:
            string = ''
            for doc_id in self.reversed_index[input_word]:
                if doc_id != 'df':
                    string += '- '+str(doc_id)+': '+self.get_title_by_doc_id(doc_id, ['.T'])+'\n'
        return string
