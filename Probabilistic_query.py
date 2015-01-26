# -*- coding: utf-8 -*-

# Imports
# -------
from collections import defaultdict
from Query import Query
from math import log10
import re

# Class
# ------------------------------


class Probabilistic_query(Query):
    """ Probabilistic query """

    def indexize(self, query):
        """ transform the query from a string to a word index """
        query_index = defaultdict(int)
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+", query)
        for word in wordsBuffer:
            word = word.lower()
            if not self.compare(word):
                query_index[word] += 1
        return query_index

    def execute_query(self, pond_type):
        """ executes query based on probabilistic model """
        # p is set to 0.66 = approximately 2/3.
        p = 0.66
        log_p = log10(p/(1-p))

        # Computes Retrieval Status Value
        res_temp = defaultdict(float)
        rsv = 0
        for w in self.indexed_query:
            if w in self.my_index.reversed_index:
                for doc_id in self.my_index.reversed_index[w]:
                    if doc_id != 'df':
                        df = float(self.my_index.reversed_index[w]['df'])
                        N = float(int(self.my_index.N))
                        res_temp[doc_id] += log_p + log10((N-df)/df)
        return res_temp

