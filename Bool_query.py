from Config import Config
from Query import Query
import re

# Class
# ------------------------------

class Bool_query extends Query:
    """
    Represent a query

    """

    def __init__(self, query):
        self.my_query = query
        self.config = Config()
        self.indexed_query = self.indexize(query)
        self.results = []

    def __str__(self):
        return str(self.indexed_query)

    def indexize(self, query):
        query_index = {}
        wordsBuffer = re.findall(r"[a-zA-Z0-9]+",query)
        for word in wordsBuffer:
            word = word.lower()
            if not self.compare(word):
                self.populate_index(query_index, word)
        return query_index

    def populate_index(self, index, key):
        if key in index:
            index[key] += 1
        else:
            index[key] = 1

    def compare(self, element):
        if element in self.config.words:
            return True
        return False
